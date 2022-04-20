import configparser
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin


app = Flask(__name__)

config = configparser.ConfigParser()
try:
    config_location = 'coffeeCalc/etc/defaults.cfg'
    config.read(config_location)
  
    app.config['DEBUG'] = config.get('config', 'debug')
    app.config['ip_address'] = config.get('config', 'ip_address')
    app.config['port'] = config.get('config', 'port')
    app.config['url'] = config.get('config', 'url')
    app.secret_key = config.get('config', 'secret_key')
        
    app.config['log_file'] = config.get('logging', 'file')
    app.config['log_location'] = config.get('logging', 'location')
    app.config['log_level'] = config.get('logging', 'level')
except Exception as e:
    print(e)
    print('Could not read config file from ' + config_location)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['IMAGE_UPLOADS'] = 'coffeeCalc/static/profile_images'

db = SQLAlchemy(app)

'''
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='client', lazy=True)
    notes = db.relationship('Note', backref='client', lazy=True)

    def __repre__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    start_country = db.Column(db.String(100), nullable=False)
    origin_to_port_distance = db.Column(db.String(100), nullable=False)
    end_location = db.Column(db.String(100), nullable=False)
    port_to_client_distance = db.Column(db.String(100), nullable=False)
    weight = db.Column(db.String(100), nullable = False)
    carbon_cost = db.Column(db.String(100), nullable=True)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    note_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Note('{self.content}')"

class Country(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.Text, nullable = False)
    region = db.Column(db.Text, nullable = False)
    port = db.Column(db.Text, nullable = False)
    region_to_port_cost = db.Column(db.Integer, nullable = False)
    port_to_UK_cost = db.Column(db.Integer, nullable = False)

    def __repr__(self):
        return f"Country('{self.title}')"




'''

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

log_pathname = app.config['log_location'] + app.config['log_file']
file_handler = RotatingFileHandler(log_pathname, maxBytes = 1024 * 1024 * 10, backupCount = 1024)
file_handler.setLevel(app.config['log_level'])
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
file_handler.setFormatter(formatter)
app.logger.setLevel(app.config['log_level'])
app.logger.addHandler(file_handler)

from coffeeCalc import routes