# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(testing=False, database_uri=None):
    app = Flask(__name__)
    app.config['TESTING'] = testing
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri or 'sqlite:///bookstore.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    # from .views import bp as main_bp  # if you use blueprints
    # app.register_blueprint(main_bp)

    return app
