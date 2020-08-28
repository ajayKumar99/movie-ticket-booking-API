from flask import Flask
import os
from .extensions import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .routes import middleware

    app.register_blueprint(middleware)

    @app.route('/')
    def index():
        return '<h1>Movie Ticket Booking API</h1>'

    return app