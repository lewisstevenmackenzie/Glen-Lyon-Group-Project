from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required, UserMixin


app = Flask(__name__)

app.config['SECRET_KEY'] = '8656d430a91e21e849364b1dadde70eb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)


posts = [
        {
            'athlete': 'Lewis Mackenzie',
            'title': 'Run',
            'content': 'I ran 5km',
            'date':'July 10th 2021'
        },
        {
            'athlete': 'Harry Mackenzie',
            'title': 'Cycle',
            'content': 'I cycled 20km',
            'date':'July 15th 2021'
        },

        ]

if __name__ == "__main__":
    app.run(debug=True)