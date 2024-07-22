from flask import Flask
from .config import ApplicationConfig
from flask_session import Session

def create_app():
    auth = Flask(__name__, template_folder='templates')

    auth.secret_key = ApplicationConfig.SECRET_KEY
    auth.config.from_object(ApplicationConfig)

    # Enable secure serverside session
    #server_session = Session(auth)

    # Blueprint for auth routes
    from .authentication import bp as auth_bp
    auth.register_blueprint(auth_bp)

    # Blueprint for non-auth parts of the auth
    from .profile import bp as profile_bp
    auth.register_blueprint(profile_bp)

    return auth
