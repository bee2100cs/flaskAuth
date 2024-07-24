from flask import Blueprint, session, g
from ..config import ApplicationConfig
import pyrebase

# Create the blueprint isntance
main = Blueprint('main', __name__)

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)
db = firebase.database()

@main.before_app_request
def load_user():
    #  Store user data in Flask's global `g` object
    if 'user' in session and 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('users').child(user_id).get().val()
        g.user_data = user_data
    else:
        g.user_data = None


# Import the routes to register them with the blueprint
from . import routes