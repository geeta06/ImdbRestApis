''' This is main app file for project'''
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from .views import main
    from .auth_views import auth_blueprint
    app.register_blueprint(main)
    app.register_blueprint(auth_blueprint)

    return app
