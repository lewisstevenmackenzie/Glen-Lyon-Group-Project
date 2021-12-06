from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_wtf.file import FileField, FileRequired, FileAllowed
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max = 10)])

    email = StringField('email', validators=[DataRequired(), Email()])
    
    password = PasswordField('password', validators=[DataRequired()])
    
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])

    profilepic = FileField(validators=[ FileRequired(), FileAllowed(['jpg'], 'Only jpg!') ])

    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    
    email = StringField('email', validators=[DataRequired(), Email()])

    password = PasswordField('password', validators=[DataRequired()])

    remember = BooleanField('Remember Me') 

    submit = SubmitField('Login')