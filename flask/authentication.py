import pyrebase
import os
from dotenv import load_dotenv
import os
from flask import Blueprint, session, render_template, request, redirect, url_for

load_dotenv()

bp = Blueprint("authentication", __name__)

# firebase config
config = {
    'apiKey': os.environ.get("apiKey"),
    'authDomain': os.environ.get("authDomain"),
    'projectId': os.environ.get("projectId"),
    'storageBucket': os.environ.get("storageBucket"),
    'messagingSenderId': os.environ.get("messagingSenderId"),
    'appId': os.environ.get("appId"),
    'measurementId': os.environ.get("measurementId"),
    'databaseURL': ""
}

# Initialize firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

# email = 'test@gmail.com'
# password = '1234567'

# Create a new user
#user = auth.create_user_with_email_and_password(email, password)
#print(user)

# Sign in user
@bp.route('/', methods=['POST', 'GET'])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # Return greeting after login
            return 'Hi, {}'.format(session['user'])
        except:
            return 'Failed to login'
    return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@bp.route('/check_login')
def check_login():
    if 'user' in session:
        return 'Hi, {}'.format(session['user'])
    else:
        return 'Please log in'
    

# # Get user info
# info = auth.get_account_info(user['idToken'])

# # Verify email
# auth.send_email_verification(user['idToken'])

# # Reset password
# auth.send_password_reset_email(email)