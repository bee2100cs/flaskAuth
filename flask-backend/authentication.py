import pyrebase
import os
from dotenv import load_dotenv
import os
from flask import Blueprint, session, render_template, request, redirect, url_for
from .config import ApplicationConfig


load_dotenv()

bp = Blueprint("authentication", __name__)

# firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up authentication manager
auth = firebase.auth()


# Create a new user
#user = auth.create_user_with_email_and_password(email, password)
#print(user)

# Sign in user
@bp.route('/login', methods=['POST', 'GET'])
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
            return 'Invalid user or password'
    return redirect(url_for('main.index'))

@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        # confirmpass = request.form.get('confirmPass')

        try:
            auth.create_user_with_email_and_password(email, password)
            return('Welcome!')
        except:
            return("Email already exists")

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
