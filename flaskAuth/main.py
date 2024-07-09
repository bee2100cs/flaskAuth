from flask import Flask, Blueprint, session, render_template, request, redirect, url_for, jsonify
from .config import ApplicationConfig
import pyrebase


bp = Blueprint("main", __name__)

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up database
db = firebase.database()


@bp.route("/")
def index():
    
    return render_template('home.html')

@bp.route('/onboarding')
def onboarding():
    if 'user' in session and 'user_id' in session:
        user_email = session['user']
        user_id = session['user_id']

        # Fetch user data from Firebase
        user_data = db.child('users').child(user_id).get().val()

        return render_template('onboarding.html', user_email=user_email, user_id=user_id, user_data=user_data)
    else:
        return redirect(url_for('authentication.login'))  # Redirect to login if not logged in

@bp.route("/validate_username", methods=["POST"])
def validate_username():
    if 'user' in session and 'user_id' in session:
        user_id = session["user_id"]
        username = request.json["username"].lower()
        # Check if username already exists
        # Note: define the index for username in the database rules for this to work
        existing_username = db.child('users').order_by_child('username').equal_to(username).get().val()
        if not existing_username:
            return jsonify({"exists": False}), 200
        else:
            for key, value in existing_username.items():
                #Ensure that it's not the same user
                if key != user_id: 
                    return jsonify({"exists": True}), 200
                else:
                    return jsonify({"exists": False}), 200
        
            


@bp.route("/onboarding", methods=['POST','GET'])
def onboarding_callback():
    
    if 'user' in session and 'user_id' in session:
        user_id = session['user_id']

        # User data from Onboarding form
        username = request.json['username'].lower()
        name = request.json['name']
        country = request.json['country']
        dob = request.json['dob']
        gender = request.json['gender']
        ethnicity = request.json['ethnicity']
        industry = request.json["industry"]
        jobFunction = request.json["jobFunction"]
        seniority = request.json["seniority"]
        salary = request.json["salary"]
        education = request.json["education"]
        
        # dictionary for professional info:
        professional_info = {
        "industry": industry,
        "jobFunction": jobFunction,
        "seniority": seniority,
        "salary": salary,
        "education": education
        }

        print(f'Username: {username}')
        print(f'Name: {name}')
        print(f'Country: {country}')
        #print(f'Date of Birth: {dob}')
        # Check if username already exists
        # Note: define the index for username in the database rules for this to work
        existing_username = db.child('users').order_by_child('username').equal_to(username).get().val()
        if existing_username:
            for key, value in existing_username.items():
                if key != user_id: #Ensure that it's not the same user
                    return jsonify({'message': "username already exists. Please choose a different username.", 'redirect_url':None })
        
        #Update user data in Firebase Database
        db.child('users').child(user_id).update({
            "username": username,
            'name': name,
            'country':country,
            'dob':dob, 
            'gender':gender,
            'ethnicity':ethnicity,
            "professional_info":professional_info,
            'first_login': True
            })

        return jsonify({'message': 'Onboarding completed', 'redirect_url':url_for('main.profile')})
    else:
        # Redirect to login if not logged in
        return redirect(url_for('authentication.login')) 


@bp.route("/profile")
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('authentication.login'))

@bp.route("/search")
def search():

    return render_template('search.html')