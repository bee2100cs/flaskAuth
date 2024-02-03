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
        user = auth.sign_in_with_email_and_password(email, password)
        session['user'] = email
        # Return greeting after login
        return jsonify({'redirect_url': url_for('main.home'), 'message': 'You Are Logged In'})
        
    except:
        return jsonify({'redirect_url': None, 'message': 'Invalid user or password'})
    
    #return redirect(url_for('main.index'))

@bp.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')
    


# # Sign in user
# @bp.route('/login', methods=['POST', 'GET'])
# def login():
#     if('user' in session):
#         return 'Hi, {}'.format(session['user'])
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         try:
#             user = auth.sign_in_with_email_and_password(email, password)
#             session['user'] = email
#             # Return greeting after login
#             return 'Hi, {}'.format(session['user'])
#         except:
#             return 'Invalid user or password'
#     return redirect(url_for('main.index'))

# @bp.route('/signup', methods=['POST', 'GET'])
# def signup():
#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')

#         # Check password length
#         if len(password) < 6:
#             flash("Password must be at least six characters long", "error")
#             return redirect(url_for('main.index'))
        
#         try:
#             auth.create_user_with_email_and_password(email, password)

#             # Create a session id to login user once they register
#             session["user"] = email
#             # Redirect the user to a welcome page or any desired page
#             return redirect(url_for('authentication.welcome'))
#         except:
#             return("Email already exists")
        
# @bp.route('/welcome')
# def welcome():
#     if 'user' in session:
#         user_email = session['user']
#         return render_template('welcome.html', user_email=user_email)
#     else:
#         return redirect(url_for('authentication.login'))  # Redirect to login if not logged in

# @bp.route('/logout')
# def logout():
#     session.pop('user')
#     return redirect('/')
    

# # Get user info
# info = auth.get_account_info(user['idToken'])

# # Verify email
# auth.send_email_verification(user['idToken'])

# # Reset password
# auth.send_password_reset_email(email)
