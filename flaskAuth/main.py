from flask import Flask, Blueprint, session, render_template, request, redirect, url_for, jsonify
from .config import ApplicationConfig
import pyrebase
from .authentication import login_required
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
import urllib


bp = Blueprint("main", __name__)

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up database
db = firebase.database()
storage = firebase.storage()




@bp.route("/")
def index():
    
    return render_template('home.html')

@bp.route('/onboarding')
@login_required
def onboarding():

    user_email = session['user']
    user_id = session['user_id']

    # Fetch user data from Firebase
    user_data = db.child('users').child(user_id).get().val()
    professions = db.child("data").child("profession_data").child("professions").get().val()
    industries = db.child("data").child("profession_data").child("industries").get().val()
    education = db.child("data").child("profession_data").child("education").get().val()
    seniority = db.child("data").child("profession_data").child("seniority").get().val()
    salary = db.child("data").child("profession_data").child("salary range").get().val()
    countries_raw = db.child("data").child("countries").get().val()
    countries = dict(sorted(countries_raw.items(), key=lambda item: item[1]))
    countries = sorted(countries.values())

    return render_template('onboarding.html', 
                           user_email=user_email,
                           user_id=user_id,
                           user_data=user_data,
                           countries=countries,
                           industry=industries,
                           education=education,
                           seniority=seniority,
                           salary=salary,
                           professions=professions
                           )


@bp.route("/validate_username", methods=["POST"])
@login_required
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
        profession = request.json["profession"]
        seniority = request.json["seniority"]
        salary = request.json["salary"]
        education = request.json["education"]
        
        # dictionary for professional info:
        professional_info = {
        "industry": industry,
        "profession": profession,
        "seniority": seniority,
        "salary": salary,
        "education": education
        }
        #Update user data in Firebase Database
        db.child('users').child(user_id).update({
            "username": username,
            'name': name,
            'country':country,
            'dob':dob, 
            'gender':gender,
            'ethnicity':ethnicity,
            "professional_info":professional_info,
            'first_login_done': True
            })

        return jsonify({'message': 'Onboarding completed', 'redirect_url':url_for('main.profile')})
    else:
        # Redirect to login if not logged in
        return redirect(url_for('authentication.login')) 
    

@bp.route("/profile")
@login_required
def profile():
    user_id = session['user_id']
    user_data = db.child("users").child(user_id).get().val()
    #user_data = db.child("users").order_by_child("username").equal_to(username).get().val()
    if user_data:
        # Safe access to 'professional_info dictionary
        professional_info = user_data.get('professional_info', {})
        personal_info_fields = [
            ('Full name', user_data.get('name')),
            ('Email', user_data.get('email')),
            ('Phone', user_data.get('phone')),
            ('Gender', user_data.get('gender')),
            # Convert enthinicity list to a comma-separated string
            ('Ethnicity', ', '.join(user_data['ethnicity']) if isinstance(user_data.get('ethnicity'), list) else user_data.get('ethnicity')),
            ('dob', user_data.get('dob')),
            ('Address', user_data.get('address')),
            ('Country', user_data.get('country'))
        ]
        job_info_fields = [
            ('Industry', professional_info.get('industry')),
            ('Profession', professional_info.get('profession')),
            ('Seniority', professional_info.get('seniority')),
            ('Salary', professional_info.get('salary')),
            ('Education', professional_info.get('education'))
        ]

        # Filter out fields with None values
        personal_info_fields = [field for field in personal_info_fields if field[1] is not None]
        job_info_fields = [field for field in job_info_fields if field[1] is not None]

        return render_template('profile.html', user=user_data, personal_info_fields=personal_info_fields, job_info_fields = job_info_fields)
    else:
        # Handle case where user data is not found
        return "User data not found", 404

@bp.route("/profile/<username>")
def public_profile(username):
        
        # Fetch user data from Firebase realtime database
        user_data = db.child('users').order_by_child("username").equal_to(username).get()
        if user_data.each():
            user = list(user_data.each())[0].val()
            return render_template('profile.html', user=user)
        else:
            return "User not found", 404
        


@bp.route("/edit_profile")
@login_required
def edit_profile():
    user_id = session['user_id']
    user_data = db.child('users').child(user_id).get().val()
    countries_raw = db.child("data").child("countries").get().val()
    countries = dict(sorted(countries_raw.items(), key=lambda item: item[1]))
    countries = sorted(countries.values())
    professional_info = user_data.get('professional_info', {})
    professions = db.child("data").child("profession_data").child("professions").get().val()
    industries = db.child("data").child("profession_data").child("industries").get().val()
    education = db.child("data").child("profession_data").child("education").get().val()
    seniority = db.child("data").child("profession_data").child("seniority").get().val()
    salary = db.child("data").child("profession_data").child("salary range").get().val()
    return render_template('edit-profile.html', 
                           user= user_data, 
                           countries=countries, 
                           professional_info=professional_info,
                           professions=professions,
                           education=education,
                           industries=industries,
                            seniority=seniority,
                            salary=salary )

@bp.route('/edit_profile', methods=['POST'])
@login_required
def edit_profile_callback():
    user_id = session['user_id']
    try:
        # Parse the incoming data
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        print(data)

        professional_info_fields = {'industry', 'profession', 'seniority', 'education', 'salary'}

        for key, value in data.items():
            if key != 'user_id':
                if key in professional_info_fields:
                    db.child('users').child(user_id).child("professional_info").update({key: value})
                else:
                    db.child('users').child(user_id).update({key: value})
        
        return jsonify({'message': ' Profile updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'profilePic' not in request.files:
        return 'No file part'
    file = request.files['profilePic']
    if file.filename =='':
        return 'No selected file'
    
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join('/tmp', filename)
        file.save(file_path)
        storage.child('profile_pics').child(filename).put(file_path)
        # Get url to profile pic
        url = storage.child('profile_pics').child(filename).get_url(None)
        os.remove(file_path)

        # Save the download URL in the realtime Database
        user_id = session['user_id']
        db.child('users').child(user_id).update({'profile_pic_url': url})
        return jsonify({'message': 'File uploaded successfuly', 'redirect_url': url} )
    return jsonify({'message': 'File upload falied'}), 500

@bp.route("/search")
def search():

    return render_template('search.html')