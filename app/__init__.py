from flask import Flask
from flask_session import Session
from app.auth import create_app as create_auth_app
from .config import ApplicationConfig
from app.main import main as main_bp


def create_app():
    app = Flask(__name__)

    app.secret_key = ApplicationConfig.SECRET_KEY
    app.config.from_object(ApplicationConfig)

    Session(app)

    # Register the main blueprint
    app.register_blueprint(main_bp)

    # Intialie the auth app and register blueprint
    auth_app = create_auth_app()
    for blueprint in auth_app.blueprints.values():
        if blueprint.name == "authentication":
            app.register_blueprint(blueprint, url_prefix='/auth')
        else:
            app.register_blueprint(blueprint)

    return app