from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    TextField,
    TextAreaField,
    PasswordField,
    BooleanField,
    ValidationError
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

    username = StringField('Username', [DataRequired(), Length(max=255)])
    password = PasswordField('Password', [DataRequired(), Length(min=4)])
    comfirm = PasswordField('Confirm Password', [DataRequired(), EqualTo('password')])

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