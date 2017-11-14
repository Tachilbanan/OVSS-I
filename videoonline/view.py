from flask import Blueprint, request, render_template, flash, redirect, url_for, send_from_directory, send_file
from videoonline.extensions import cache
from videoonline.forms import LoginForm, RegisterForm
from videoonline.models import db, User, Video, Classify
from flask_login import login_user, logout_user, login_required
from flask_principal import identity_changed, Identity, current_app, AnonymousIdentity


root_view = Blueprint("/", __name__)


def make_cache_key(*args, **kwargs):
    """Dynamic creation the request url."""

    path = request.path
    args = str(hash(frozenset(request.args.items())))
    return (path + args).encode('utf-8')


@root_view.route('/')
@root_view.route('/<int:page>')
def home(page=1):
    """View function for home page"""
    videos = Video.query.order_by(
        Video.c_time.desc()
    ).paginate(page, 10)

    recent, top_classifys = sidebar_data()

    return render_template('home.html',
                           videos=videos,
                           recent=recent,
                           top_classifys=top_classifys)


@root_view.route('/video/<string:video_id>')
def video(video_id):
    """View function for post page"""

    video = db.session.query(Video).get_or_404(video_id)
    classifys = video.classifys
    recent, top_classifys = sidebar_data()

    return render_template('video.html',
                           video=video,
                           classify=classifys,
                           recent=recent,
                           top_classifys=top_classifys
                           )


@root_view.route('/play/<string:video_id>')
def play(video_id):
    video = Video.query.filter_by(id=video_id).all()
    if not video != []:
        return render_template('40X/404.html'), 404
    filename = video[0].filename
    return send_from_directory('theme/static/videos/', filename=filename)


@root_view.route('/classify/<string:classify_name>')
def classify(classify_name):
    """View function for classify page"""

    classifys = db.session.query(Classify).filter_by(name = classify_name).first_or_404()
    videos = classifys.videos.order_by(Video.publish_date.desc()).all()
    recent, top_classifys = sidebar_data()

    return render_template('classify.html',
                           classifys=classifys,
                           videos=videos,
                           recent=recent,
                           top_classifys=top_classifys)


# 侧边栏数据
@cache.cached(timeout=7200, key_prefix='sidebar_data')
def sidebar_data():
    """Set the sidebar function."""

    # Get Video of recent
    recent = db.session.query(Video).order_by(
            Video.c_time.desc()
        ).limit(5).all()

    # 获取分类
    top_classifys = db.session.query(Classify).all()
    return recent, top_classifys


@root_view.route('/login', methods=['GET', 'POST'])
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()

        # 登入用户
        # login_user(user, remember = form.remember.data)
        # 都是管理员 设置记住身份应该不合适
        login_user(user)

        # 防止next异常、攻击、等各种，具体根据自己的需要去写。
        # if not next_is_valid(next):
        #     return abort(400)

        # 改变用户身份
        identity_changed.send(
            current_app._get_current_object(),
            identity=Identity(user.id),
        )

        flash("You have been logged in.", category="success")
        return redirect(url_for('admin.home'))

    return render_template('login.html',
                           form=form)


@root_view.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """View function for logout."""

    # 登出用户
    logout_user()

    # 改变用户身份
    identity_changed.send(
        current_app._get_current_object(),
        identity=AnonymousIdentity())

    flash("You have been logged out.", category="success")
    return redirect(url_for('/.home'))

