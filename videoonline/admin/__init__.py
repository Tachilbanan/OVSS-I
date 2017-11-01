from flask import Blueprint, request, render_template, flash, redirect, url_for, abort
from videoonline.forms import LoginForm, RegisterForm
from videoonline.models import db, User, Video, Classify
from uuid import uuid4
from flask_login import login_user, logout_user, login_required, login_manager, current_user
from flask_principal import Identity, AnonymousIdentity, identity_changed, current_app, Permission, UserNeed
from videoonline.extensions import superadmin_permission, admin_permission, helper_permission


admin_view = Blueprint('admin', __name__)

@admin_view.route('/')
@login_required
def home():
    user = current_user.username
    p = current_user.roles.name
    return render_template('admin/home.html', user = user, p = p)

@admin_view.route('/ad')
@login_required
def ad():
    # 这里用 @login_required 装饰器实现
    # # Ensure the user logged in.
    # if not current_user:
    #     return redirect(url_for('admin.login'))

    # 检查权限，如果权限符合 则正常处理，否则返回信息权限不足
    permission = Permission(UserNeed(current_user))
    if admin_permission.can() or superadmin_permission.can():
        # if current_user != post.users:
        #    abort(403)

        user = current_user.username
        p = current_user.roles.name
        return render_template('admin/user/home.html',user=user,p = p)
    else:
        # abort(403)
        return render_template('40X/403.html', re = url_for('admin.home'))

@admin_view.route('/login', methods=['GET', 'POST'])
def login():
    """View function for login."""

    # Will be check the account whether rigjt.
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).one()

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
            identity = Identity(user.id),
        )

        flash("You have been logged in.", category="success")
        return redirect(url_for('admin.home'))

    return render_template('admin/login.html',
                           form = form)


@admin_view.route('/logout', methods = ['GET', 'POST'])
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

@admin_view.route('/register', methods=['GET', 'POST'])
def register():
    """View function for Register."""

    # Will be check the username whether exist.
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username = form.username.data,
                        password = form.password.data,
                        )

        db.session.add(new_user)
        db.session.commit()

        flash('Your user has been created, please login.',
              category = "success")

        return redirect(url_for('admin.login'))
    return render_template('admin/register.html',
                           form = form)

@admin_view.route('/user/<string:username>')
@login_required
def user(username):
    """View function for user page"""
    user = db.session.query(User).filter_by(username = username).first_or_404()

    return render_template('user.html', user = user)