from flask import Flask
from config.settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Register routes
    from .routes import register_routes
    register_routes(app)

    return app