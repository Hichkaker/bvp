from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import controller, models
#import keen

#keen.project_id = "562c0a6ae08557197095f938 "
#keen.write_key = """bab669a1b3ba8f496da5a00e45b4b2545229c191f8520c5fd6d2f1619cd56ef48ee8a23649838a29bee8be1ba1e1d933dd4242326ad78d0d1d6d59a697befb15b677282e4f83d3a538431b7d1ebb29bdff6c115cfb4234ecc182f46ee9eb86ab3f81a0f18c6b8201c6acb0c4e904be55"""
#keen.master_key = "424187B8FE3D1213FAB900E7F3655737"