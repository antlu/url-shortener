import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from url_shortener.settings import config, ImproperlyConfigured


env = os.getenv('FLASK_ENV')

db = SQLAlchemy()

def create_app(config_name=env):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    if not app.config['SECRET_KEY']:
        raise ImproperlyConfigured("No SECRET_KEY set", env)

    db.init_app(app)

    from url_shortener.views import bp
    app.register_blueprint(bp)

    return app
