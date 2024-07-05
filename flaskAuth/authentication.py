from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, flash
from .config import ApplicationConfig
import pyrebase
from flask_session import Session
from functools import wraps

bp = Blueprint("authentication", __name__)

# firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up authentication manager
auth = firebase.auth()

@bp.route('/api/signup')
def signup():
    return render_template("signup.html")

@bp.route('/api/signup', methods=["POST", "GET"])
def signup_callack():
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
       return jsonify({'redirect_url': None, 'message': 'Password must be at least six characters long'}), 400
    try:
        user = auth.create_user_with_email_and_password(email, password)
        
        # # Store user information in session
        # session["user"] = {
        #     'email': email,
        #     'idToken': user['idToken']
        # }
        
        # send email verification
        auth.send_email_verification(user['idToken'])
        flash("Congratulations! You've been signed up. Please verify your email address before logging in.", "success")
        # Redirect to login page
        return jsonify({'redirect_url': url_for('authentication.login'), 'message': "SUCCESS! You have been registered. Please verify your email address before logging in."})

    except:
        return jsonify({'message': "Email already exists!"})

@bp.route('/api/login')
def login():
   
    return render_template('login.html')

# Sign in user
@bp.route('/api/login', methods=['POST', 'GET'])
def login_callback():
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
        id = user['idToken']

        userverify = auth.get_account_info(id)
        
        # # Check if the email is verified
        user_verified = userverify['users'][0]['emailVerified']
        
        if user_verified:
            # Email is verified, proceed to the main.index page

            session["user"] = email
            # # Redirect the user to a welcome page or any desired page
            if 'first_login' not in session:
                session['first_login'] = True

                return jsonify({'redirect_url': url_for('main.onboarding'), 'message': 'First login successful'})
            else:
                return jsonify({'redirect_url': url_for('main.index'), 'message': 'Login successful'})
        else:
            # Email is not verified, notify the user
            return jsonify({'redirect_url': None, 'message': 'Please verify your email before proceeding.'})


    except:
        return jsonify({'redirect_url': None, 'message': 'Invalid email or password!!!!'})
        
# Reset Password    
@bp.route('/api/reset', methods=['POST'])
def reset_pass():
    email = request.json['email']
    # Check if the email exists in your firebase user database and send reset link
    try:
        auth.send_password_reset_email(email)
        return jsonify({"message":'Password reset email sent'})
    except:
        return jsonify({"Message":'Invalid Email'}), 400

@bp.route('/api/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'GET':
        session.pop('user')
        return redirect(url_for('main.index'))
    else:
        return jsonify({'error': 'Method not allowed'}), 405  # Return a 405 Method Not Allowed status for other methods
