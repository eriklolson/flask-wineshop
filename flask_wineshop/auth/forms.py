from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(), Length(min=4, max=20, message='Username must be between 4 and 20 characters long.')])
    password = PasswordField('Password', validators=[
            DataRequired(), Length(min=8, max=80, message='Password must be between 8 and 80 characters long.')])
    submit = SubmitField('Sign In')


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
            DataRequired(),
            Length(min=4, max=20, message='Username must be between 4 and 20 characters long.')])
    email = StringField('Email', validators=[
            DataRequired(),
            Email(message='Please enter a valid email.'), Length(max=50)])
    password = PasswordField('Password', validators=[
            DataRequired(),
            Length(min=8, max=80, message='Please select a password between 8 and 80 characters.')])
    confirmPassword = PasswordField('Confirm Password', validators=[
            DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Register')
