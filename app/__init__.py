from flask import Flask
from ..config import ApplicationConfig

def create_app():
    app = Flask(__name__)

    app.secret_key = ApplicationConfig.SECRET_KEY
    app.config.from_object(ApplicationConfig)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app