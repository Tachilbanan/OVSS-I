from flask import Blueprint, render_template
from flask_login import login_required
from videoonline.models import db, User, Video, Classify

admin_view = Blueprint('admin', __name__)


@admin_view.route('/')
@login_required
def home():
    return render_template('admin/home.html')


@admin_view.route('/video')
@login_required
def video():
    _video = Video.query.all()
    return render_template('admin/video.html', video=_video)


@admin_view.route('/user')
@login_required
def user():
    _user = User.query.all()
    return render_template('admin/user.html', user=_user)


@admin_view.route('/classify')
def classify():
    _classify = Classify.query.all()
    return render_template('admin/classify.html', classify=_classify)
