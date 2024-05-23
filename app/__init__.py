from flask import Flask
from flask_pymongo import PyMongo
from app.api import bp as api_bp
import logging
import os


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    mongo = PyMongo(app)
    app.mongo = mongo

    app.register_blueprint(api_bp)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    handler = logging.FileHandler('logs/app.log')
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)

    return app
