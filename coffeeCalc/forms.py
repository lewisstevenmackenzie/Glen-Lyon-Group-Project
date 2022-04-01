from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from coffeeCalc.models import User

class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max = 10)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_country = TextAreaField('Origin Country', validators=[DataRequired()])
    origin_to_port_distance = TextAreaField('Distance to port', validators=[DataRequired()])
    end_location = TextAreaField('End Location', validators=[DataRequired()])
    port_to_client_distance = TextAreaField('Distance to client', validators=[DataRequired()])
    weight = TextAreaField('Weight', validators=[DataRequired()])
    submit = SubmitField('Post')

class AccountForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    

class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')