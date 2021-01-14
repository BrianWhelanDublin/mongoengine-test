from flask_wtf import FlaskForm
from wtforms import (StringField,
                     PasswordField,
                     BooleanField,
                     SubmitField,
                     TextAreaField)
from wtforms.validators import (ValidationError,
                                DataRequired,
                                Email,
                                EqualTo,
                                Length)
from flask_login import current_user
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.objects(
            username=username.data).first()
        if user is not None:
            raise ValidationError("Username already used!")

    def validate_email(self, email):
        user = User.objects(
            email=email.data).first()
        if user is not None:
            raise ValidationError("Email already used!")


class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.objects(
                username=username.data).first()
            if user:
                raise ValidationError("Username Already Taken")


class PostForm(FlaskForm):
    post = TextAreaField("Say something", validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField("Submit")
