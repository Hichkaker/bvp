from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import controller, models
handler = RotatingFileHandler('geo.log', maxBytes=10000, backupCount=1)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
