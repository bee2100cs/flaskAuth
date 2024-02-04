import pyrebase
from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, flash
from .config import ApplicationConfig
from flask_session import Session
from functools import wraps

bp = Blueprint("authentication", __name__)

# firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up authentication manager
auth = firebase.auth()

@bp.route('/api/signup', methods=["POST", "GET"])
def signup():
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
       return jsonify({'redirect_url': None, 'message': 'Password must be at least six characters long'}), 400
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        # Store user information in session
        session["user"] = {
            'email': email,
            'idToken': user['idToken']
        }
        # Redirect user to the verification route
        return redirect(url_for('authentication.verify'))

    except:
        return jsonify({'message': "Email already exists!"})

# Verify email
@bp.route('/verify')
def verify():
    # Retrieve user information from session
    user_data = session.get("user")
    if user_data is None:
        return jsonify({'error': 'User data not found in session'}), 400
    

    user = auth.get_account_info(user_data['idToken'])
    try:        
        if not user['users'][0]['emailVerified']:

            # Send email verification
            auth.send_email_verification(user_data['idToken'])
            return jsonify({"message":"Email verification sent!"})
        
        # If email is already verified, redirect to homepage
        return jsonify({'redirect_url': url_for('main.welcome'), 'message': 'Signup successful'})
    except auth.AuthError as e:
        return jsonify({'error': 'Error retrieving user info: {}'.format(e)}), 500


# Sign in user
@bp.route('/api/login', methods=['POST', 'GET'])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    
    email = request.json['email']
    password = request.json['password']
    try:
         # Sign in user
        user = auth.sign_in_with_email_and_password(email, password)
        # before the 1 hour expiry:
        user = auth.refresh(user['refreshToken'])
        # now we have a fresh token
        user['idToken']
        session["user"] = email
        # # Redirect the user to a welcome page or any desired page
        return jsonify({'redirect_url': url_for('main.welcome'), 'message': 'Login successful'})

    except auth.InvalidEmailError:
        return jsonify({'redirect_url': None, 'message': 'Invalid email or password'}), 400
    except auth.WrongPasswordError:
        return jsonify({'redirect_url': None, 'message': 'Invalid email or password'}), 400
    
    #return redirect(url_for('main.index'))

@bp.route('/api/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        session.pop('user')
        return jsonify({'redirect_url': url_for('main.index'), 'message': 'Logout successful'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405  # Return a 405 Method Not Allowed status for other methods
