from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, DecimalField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

# Form used by the signup html page to validate a new user
class SignUpForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max = 10)])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

# Form validates a user when logging in
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember = BooleanField('Remember Me') 
    submit = SubmitField('Login')

# Form to validate a logged in user enetering a new coffee route
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    start_country = SelectField("Origin Country")    
    origin_to_port_distance = DecimalField('Distance to port (km)', validators=[DataRequired(), NumberRange(min=0)])
    end_location = TextAreaField('End Location', validators=[DataRequired()])
    port_to_client_distance = DecimalField('Tillbiry Docks to client (km)', validators=[DataRequired(), NumberRange(min=0)])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Post')

# Form to validate a non-logged in user carrying out a quick co2 calculation
class QuickCalcForm(FlaskForm): 
    start_country = SelectField("Origin Country")
    origin_to_port_distance = DecimalField('Distance to port (km)', validators=[DataRequired(), NumberRange(min=0)])
    port_to_client_distance = DecimalField('Tillbury Docks to client (km)', validators=[DataRequired(), NumberRange(min=0)])
    weight = DecimalField('Weight (kg)', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Submit')
    
# Form to create a note
class NoteForm(FlaskForm):
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')