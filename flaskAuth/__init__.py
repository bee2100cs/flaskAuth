from flask import Flask
from .config import ApplicationConfig
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.secret_key = ApplicationConfig.SECRET_KEY
    app.config.from_object(ApplicationConfig)

    # Enable secure serverside session
    server_session = Session(app)

    # Initialize extensions
    db.init_app(app)
    # Blueprint for auth routes
    from .authentication import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Blueprint for non-auth parts of the app
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app
