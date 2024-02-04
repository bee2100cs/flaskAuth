import pyrebase
from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, flash
from .config import ApplicationConfig
from flask_session import Session

bp = Blueprint("authentication", __name__)

# firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up authentication manager
auth = firebase.auth()

# email = 'bee@be.bee'
# password = 12344567

## Create a new user
# user = auth.create_user_with_email_and_password(email, password)
# print(user)

@bp.route('/api/signup', methods=["POST", "GET"])
def signup():
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
       return jsonify({'redirect_url': None, 'message': 'Password must be at least six characters long'}), 400
        #return redirect(url_for('/'))
    try:
        auth.create_user_with_email_and_password(email, password)
        

        # Send email verification
        #auth.send_email_verification(user['email'])

        # Create a session id to login user once they register
        session["user"] = email
        # Redirect the user to a welcome page or any desired page
        return jsonify({'redirect_url': url_for('main.welcome'), 'message': 'Signup successful'})

    except:
        return jsonify({'message': "Email already exists!"})
    
    #return jsonify({'message': '{} signed successfully'.format(email)})

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

        # Check if the user's email is verified
        # if not user['emailVerified']:
        #     return jsonify({'redirect_url': None, 'message': 'Email not verified. Please verify your email first.'}), 400
        
        
        session["user"] = email
        # # Redirect the user to a welcome page or any desired page
        return jsonify({'redirect_url': url_for('main.welcome'), 'message': 'Signup successful'})

    except auth.InvalidEmailError:
        return jsonify({'redirect_url': None, 'message': 'Invalid email or password'}), 400
    except auth.WrongPasswordError:
        return jsonify({'redirect_url': None, 'message': 'Invalid email or password'}), 400
    
    #return redirect(url_for('main.index'))

@bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        session.pop('user')
        return jsonify({'redirect_url': url_for('main.index'), 'message': 'Logout successful'})
    else:
        return jsonify({'error': 'Method not allowed'}), 405  # Return a 405 Method Not Allowed status for other methods
