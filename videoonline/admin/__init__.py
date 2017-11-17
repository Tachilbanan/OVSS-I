from flask import Blueprint, render_template, request, abort, url_for, redirect
from flask_login import login_required
from videoonline.models import db, User, Video, Classify, Role
from videoonline.extensions import admin_permission, superadmin_permission, videos_upload,\
    md5, images_upload
from videoonline.forms import UploadForm, RegisterForm
import time
import os

admin_view = Blueprint('admin', __name__)


def file_url(filename):
    return url_for('static', filename='videos/'+filename)


@admin_view.route('/')
@login_required
def home():
    return render_template('admin/home.html')


@admin_view.route('/video')
@login_required
def video(mess=None):
    _video = Video.query.all()
    return render_template('admin/video.html', video=_video, mess=mess)


@admin_view.route('/video/add')
@login_required
def video_add():
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    form = UploadForm()
    return render_template('admin/video_add.html', form=form)


@admin_view.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    # 判断权限
    if not superadmin_permission.can():
        return render_template('40X/403.html', re=url_for('admin.home')), 403

    form = UploadForm()
    if form.validate_on_submit():
        # 这里将要对文件名进行处理 不能直接处理中文文件名
        # 获取文件名， 扩展名
        video_kz = form.video.data.filename.split('.')

        name = form.video.data.filename
        # 对文件名md5加密
        _id = md5(form.video.data.filename + str(time.time()))
        # 将md5后的文件名加上扩展名提交
        form.video.data.filename = _id + '.' + video_kz[-1]
        # 存储文件，并接受返回文件名
        filename = videos_upload.save(form.video.data)
        # 判断图片是否存在
        if form.image.data:
            image_name = form.image.data.filename.split('.')
            form.image.data.filename = md5(form.image.data.filename + str(time.time())
                                           ) + '.' + image_name[-1]
            img = images_upload.save(form.image.data)
        else:
            img = None
        # 创建对象，存入数据库
        tmp = Video(_id, name, filename, img)
        db.session.add(tmp)
        db.session.commit()
        return 'success'
    return render_template('admin/video_add.html', form=form)


@admin_view.route('/video_edit/<_id>', methods=['GET', 'POST'])
@login_required
def video_edit(_id):
    if not (superadmin_permission.can() or admin_permission.can()):
        return render_template('40X/403.html'), 403
    _video = Video.query.filter_by(id=_id).first()
    cla = Classify.query.all()
    if not _video:
        abort(404)

    if request.method == 'GET':
        return render_template('admin/video_edit.html', video=_video, cla=cla)

    this_cla = request.form.get('cla')
    this_name = request.form.get('name')
    if not len(this_name) > 0:
        mess = '视频名不能为空！'
    else:
        this_cla = Classify.query.filter_by(name=this_cla).first()
        _video.classify = this_cla
        _video.name = this_name
        db.session.add(_video)
        db.session.commit()
        mess = '视频信息修改成功！'
    return render_template('admin/video_edit.html', video=_video, cla=cla, mess=mess)


@admin_view.route('/video_delete/<_id>')
def video_delete(_id):
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    _video = Video.query.filter_by(id=_id).first()
    if not _video:
        abort(404)
    file = videos_upload.path(_video.filename)
    if _video.img_name:
        img = images_upload.path(_video.img_name)
        os.remove(img)
    os.remove(file)
    db.session.delete(_video)
    db.session.commit()
    return video(mess='视频删除成功！')


@admin_view.route('/user')
@login_required
def user(mess=None):
    _user = User.query.all()
    return render_template('admin/user.html', user=_user, mess=mess)


@admin_view.route('/user_add', methods=['GET', 'POST'])
@login_required
def user_add():
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    form = RegisterForm()
    mess = None
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        )

        db.session.add(new_user)
        db.session.commit()
        mess = '添加用户成功！'
        form.username.data = ''

        return render_template('admin/user_add.html', form=form, mess=mess)
    return render_template('admin/user_add.html', form=form)


@admin_view.route('/user_edit/<_id>', methods=['GET', 'POST'])
@login_required
def user_edit(_id):
    if not (superadmin_permission.can() or admin_permission.can()):
        return render_template('40X/403.html'), 403
    _user = User.query.filter_by(id=_id).first()
    if not _user != []:
        abort(404)
    role = Role.query.all()
    if request.method == 'GET':
        return render_template('admin/user_edit.html', user=_user, role=role)
    for i in range(1):
        if request.method == 'POST':
            username = request.form.get('username')
            thisuser = User.query.filter_by(username=username).first()
            if not thisuser == _user:
                mess = '用户名已经存在！'
                break
            password = request.form.get('password')
            re_password = request.form.get('re_password')
            if password != re_password:
                mess = '两次密码不一致！'
                break
            l = len(password)
            if 0 < l and l < 6:
                mess = '密码长度不符合！'
                break
            if len(password) != 0:
                _user.password = _user.set_password(password)
            _role = request.form.get('role')
            _role = Role.query.filter_by(name=_role).first()
            if _role:
                _user.role = _role
            _user.username = username
            db.session.add(_user)
            db.session.commit()
            mess = '修改成功！'
    return render_template('admin/user_edit.html', user=_user, role=role, mess=mess)


@admin_view.route('/user_delete/<_id>')
@login_required
def user_delete(_id):
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    _user = User.query.filter_by(id=_id).first()
    if not _user:
        abort(404)
    db.session.delete(_user)
    db.session.commit()
    return user(mess='用户删除成功！')


@admin_view.route('/classify')
@login_required
def classify(mess=None):
    _classify = Classify.query.all()
    return render_template('admin/classify.html', classify=_classify, mess=mess)


@admin_view.route('/classify_add', methods=['GET', 'POST'])
@login_required
def classify_add():
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    if request.method == 'GET':
        return render_template('admin/classify_add.html')

    _cla = request.form.get('cla')
    if _cla:
        cla = Classify(_cla)
        db.session.add(cla)
        db.session.commit()
        mess = '分类添加成功！'
    else:
        mess = '分类名为空！'

    return render_template('admin/classify_add.html', mess=mess)


@admin_view.route('/classify_edit/<_id>', methods=['GET', 'POST'])
@login_required
def classify_edit(_id):
    if not (superadmin_permission.can() or admin_permission.can()):
        return render_template('40X/403.html'), 403
    cla = Classify.query.filter_by(id=_id).first()
    if not cla:
        abort(404)
    if request.method == 'GET':
        return render_template('admin/classify_edit.html', cla=cla)

    this_name = request.form.get('name')
    if not len(this_name) > 0:
        mess = '分类名称长度不能小于1'
    else:
        cla.name = this_name
        db.session.add(cla)
        db.session.commit()
        mess = '分类名称修改成功！'
    return render_template('admin/classify_edit.html', cla=cla, mess=mess)


@admin_view.route('/classify_delete/<_id>', methods=['GET', 'POST'])
@login_required
def classify_delete(_id):
    if not superadmin_permission.can():
        return render_template('40X/403.html'), 403
    cla = Classify.query.filter_by(id=_id).first()
    if not cla:
        abort(404)
    for i in cla.videos:
        i.classify = None
    db.session.delete(cla)
    db.session.commit()
    return classify(mess='分类删除成功！')
