# import python libraries
import configparser
import logging
import json
import bcrypt

from logging.handlers import RotatingFileHandler
from functools import wraps
from flask import Flask, g, redirect, render_template, request, session, url_for, flash

# define app
app = Flask(__name__)

# initialise app
def init(app):
    config = configparser.ConfigParser()
    try:
        config_location = 'etc/defaults.cfg'
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

# initialise logging
def logs(app):
    log_pathname = app.config['log_location'] + app.config['log_file']
    file_handler = RotatingFileHandler(log_pathname, maxBytes = 1024 * 1024 * 10, backupCount = 1024)
    file_handler.setLevel(app.config['log_level'])
    formatter = logging.Formatter('%(levelname)s | %(asctime)s | %(module)s | %(funcName)s | %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.setLevel(app.config['log_level'])
    app.logger.addHandler(file_handler)

# login decorator
def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        #
        #
        if kwargs['user'] != session.get('user'):
            #
            #
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# test route
@app.route('/')
def landing():
    return 'hello world'

init(app)
logs(app)

if __name__ == "__main__":
    init(app)
    logs(app)
    app.run(host = app.config['ip_address'],
            port = int(app.config['port']))