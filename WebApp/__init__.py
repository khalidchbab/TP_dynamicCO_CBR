from flask import Flask
from .main import main,estimate


def create_app():
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'SMA'
    app.register_blueprint(main)
    app.register_blueprint(estimate)
    return app