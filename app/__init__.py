import os
from flask import Flask
from config import Config
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler


app = Flask(__name__)
app.config.from_object(Config)
app.config['MONGODB_SETTINGS']
db = MongoEngine(app)
# host = app.config["MONGO_URI"]
# db.connect(host=host)
login = LoginManager(app)
login.login_view = "login"

from app import routes, models, errors


if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')
