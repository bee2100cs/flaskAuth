from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, flash
from .config import ApplicationConfig
import pyrebase
from functools import wraps

bp = Blueprint("authentication", __name__)

# firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up authentication manager
auth = firebase.auth()

# Set up database
db = firebase.database()


# Function to check if user is logged in
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session or 'user_id' not in session:
            # Redirect to login route
            session['next_url'] = request.url
            # redirect to login route
            return redirect(url_for('authentication.login'))
        else:
            # Clear 'next_url' from session if user is logged in
            session.pop('next_url', None)

        return f(*args, ** kwargs)
    
    return decorated_function

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

        # Add user ID to the Firebase Realtime Database
        user_id = user["localId"]
        if not user_id:
            raise ValueError("localId not found in user data")
            
        db.child("users").child(user_id).set({
            "email":email,
            "first_login_done":False
            })
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
    if'user' in session:
        return 'Hi, {}'.format(session['user'])
    
    email = request.json['email']
    password = request.json['password']
    
    try:
         # Sign in user
        user = auth.sign_in_with_email_and_password(email, password)

        # before the 1 hour expiry:
        user = auth.refresh(user['refreshToken'])
        # now we have a fresh token
        id_token = user['idToken']
        #user_id = user['localId']
        user_id = user['userId']
        
        userverify = auth.get_account_info(id_token)
        
        # Get user data in firebase realtime database
        user_data = db.child('users').child(user_id).get().val()

        # # Check if the email is verified
        user_verified = userverify['users'][0]['emailVerified']
        
        if user_verified:
            
            # successful login
            session["user"] = email
            session["user_id"] = user_id
            session["id_token"] = id_token
            # # Redirect the user to onboarding page if first login
            if user_data['first_login_done'] == False:
                # Redirect user to onboarding page
                return jsonify({'redirect_url': url_for('main.onboarding'), 'message': 'First login: Go to Onboarding'})
            
            # Check for next_url cookie in the case of use of login_required 
            if 'next_url' in session:
                
                next_url = session.pop('next_url')
                
                return jsonify({'redirect_url': next_url, 'message': "Login successful"})
            # Default Redirect to home page
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

# Delete user
@bp.route('/api/delete_user', methods=['POST'])
@login_required
def delete_user():
    try:
        user_id = session['user_id']
        id_token = session["id_token"]
        password = request.json['password']

        try:

            # Reauthenticate user with password
            user = auth.sign_in_with_email_and_password(session['user'], password)
            auth.refresh(user['refreshToken'])

            # Delete user from Firebase Realtime Database
            db.child('users').child(user_id).remove()

            # Delete user from Firebase Authentication
            auth.delete_user_account(id_token)

            # Clear session after deleting user
            session.pop("user")

            return jsonify({"success": True, "message": "User profile deleted successfully.  We are sorry to see you go", "redirect_url": url_for('main.index')}), 200

        except Exception as e:
            return jsonify({"message": "Invalid password. Please try again."}), 400

        
    except Exception as e:
        return jsonify({"error":"An error occurred while trying to delete your account. Please try again."}), 400

