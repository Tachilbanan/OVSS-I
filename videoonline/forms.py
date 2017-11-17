from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from videoonline.extensions import videos_upload, images_upload
from wtforms import (
    StringField,
    SubmitField,
    PasswordField,
    BooleanField,
)
from wtforms.validators import DataRequired, Length, EqualTo, URL

from videoonline.models import User

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField("Remember Me")

    def validate(self):
        """Validator for check the account information."""
        check_validata = super(LoginForm, self).validate()

        # If validator no pass
        if not check_validata:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            self.username.errors.append('Invalid username or password.')
            return False

        # Check the password whether right.
        if not user.check_password(self.password.data):
            self.username.errors.append('Invalid username or password.')
            return False

        return True


class RegisterForm(FlaskForm):
    """Register Form."""

    username = StringField('Username', [DataRequired('用户名已经存在！'), Length(max=255)])
    password = PasswordField('Password', [DataRequired(message='密码不符合要求！'), Length(min=4)])
    comfirm = PasswordField('Confirm Password', [DataRequired(message='两次密码不一致！'), EqualTo('password')])

    def validate(self):
        check_validate = super(RegisterForm, self).validate()

        # If validator no pass
        if not check_validate:
            return False

        # Check the user whether exist.
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            self.username.errors.append('User with that name already exists.')
            return False
        return True


class UploadForm(FlaskForm):
    """upload Form."""

    video = FileField(validators=[FileAllowed(videos_upload, u'只能上传视频！'),
                                  FileRequired(u'文件未选择！'),
                                  ]
                      )
    image = FileField(validators=[FileAllowed(images_upload, '只能上传图片！')]
                      )
    submit = SubmitField(u'上传')
