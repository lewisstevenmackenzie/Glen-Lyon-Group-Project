from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, SelectField
from flask_login import current_user
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
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
    start_country = SelectField("Origin Country")    
    origin_to_port_distance = DecimalField('Distance to port (km)', validators=[DataRequired(), NumberRange(min=0)])
    end_location = TextAreaField('End Location', validators=[DataRequired()])
    port_to_client_distance = DecimalField('Tillbiry Docks to client (km)', validators=[DataRequired(), NumberRange(min=0)])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Post')

# choices=[("Mexico"),("Mariel"), ("Jamaica"), ("Hawaii"), ("Guatemala")])

class QuickCalcForm(FlaskForm):
    start_country = SelectField("Origin Country")
    origin_to_port_distance = DecimalField('Distance to port (km)', validators=[DataRequired(), NumberRange(min=0)])
    port_to_client_distance = DecimalField('Tillbury Docks to client (km)', validators=[DataRequired(), NumberRange(min=0)])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')

class AccountForm(FlaskForm):
    username = StringField('UserName', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])
    

class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')