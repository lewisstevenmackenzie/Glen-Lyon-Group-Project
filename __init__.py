import configparser
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


application = Flask(__name__)

# setup config parameters from defaults.cfg
config = configparser.ConfigParser()
try:
    config_location = '/usr/local/env/myApp/coffeeCalc/etc/defaults.cfg'
    config.read(config_location)
  
    application.config['DEBUG'] = config.get('config', 'debug')
    application.config['ip_address'] = config.get('config', 'ip_address')
    application.secret_key = config.get('config', 'secret_key')
    application.config['SQLALCHEMY_DATABASE_URI'] = config.get('config', 'dbURL')
    application.config['IMAGE_UPLOADS'] = config.get('config', 'imgURL')
        
    application.config['log_file'] = config.get('logging', 'file')
    application.config['log_location'] = config.get('logging', 'location')
    application.config['log_level'] = config.get('logging', 'level')

except Exception as e:
    print(e)
    print('Could not read config file from ' + config_location)

db = SQLAlchemy(application)

bcrypt = Bcrypt(application)
login_manager = LoginManager(application)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

log_pathname = application.config['log_location'] + application.config['log_file']
file_handler = RotatingFileHandler(log_pathname, maxBytes = 1024 * 1024 * 10, backupCount = 1024)
file_handler.setLevel(application.config['log_level'])
formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
file_handler.setFormatter(formatter)
application.logger.setLevel(application.config['log_level'])
application.logger.addHandler(file_handler)

from coffeeCalc import routes

if __name__ == '__main__':
    application.run()