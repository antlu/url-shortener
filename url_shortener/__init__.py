import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')

    db.init_app(app)

    from url_shortener.views import bp
    app.register_blueprint(bp)

    return app
