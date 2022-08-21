from flask_wtf import FlaskForm
from datetime import datetime
from wtforms import Form, IntegerField, HiddenField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField
from wtforms.validators import ValidationError, DataRequired, Length, InputRequired, Email, EqualTo, Regexp
from flask_login import login_user, current_user, logout_user, login_required

from flask_wineshop.models import *


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4)])
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', [DataRequired()])
    email = StringField('Email', validators=[
                Length(min=4), Email(message='Enter a valid email.'), DataRequired()])
    password = PasswordField('Password', validators=[
                DataRequired(), Length(min=4, message='Please select a stronger password.')])
    confirmPassword = PasswordField('Confirm Your Password', validators=[
                DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is already registered.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('This email is already registered.')

class EditUserForm(Form):
    username = StringField('username : ', validators=[DataRequired(), Regexp('[A-Za-z ]',
                                                                             message="Name can only contain letters.")])
    email = StringField('Email ID : ', validators=[DataRequired(), Length(5, 120), Email()])
    password = PasswordField('Password : ', validators=[DataRequired(), EqualTo('confirmPassword',                                                                         message="Passwords must match.")])
    confirmPassword = PasswordField('Confirm Password : ', validators=[DataRequired()])
