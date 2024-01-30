import os
from flask import Flask

def create_app():
    app = Flask(__name__)

    app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)

    # Blueprint for auth routes
    from .authentication import bp as auth_bp
    app.register_blueprint(auth_bp)

    # Blueprint for non-auth parts of the app
    from .main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

