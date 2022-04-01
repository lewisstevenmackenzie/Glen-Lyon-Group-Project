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
app.config['IMAGE_UPLOADS'] = '/home/40445231/SET09103Coursework/fit4all/static/profile_images'

db = SQLAlchemy(app)
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