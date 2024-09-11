from flask import Blueprint, session, render_template, request, redirect, url_for, jsonify, flash
from .config import ApplicationConfig
import pyrebase
from .authentication import login_required
from werkzeug.utils import secure_filename
import os
from ..main.utils.helper import  user_quizzes, calculate_quiz_stats


bp = Blueprint("profile", __name__)

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

# Initialize firebase
firebase = pyrebase.initialize_app(config)

# Set up database
db = firebase.database()
storage = firebase.storage()




@bp.route("/")
def index():
    if 'user' in session and 'user_id' in session:
        user_id = session['user_id']
        user_data = db.child('users').child(user_id).get().val()
        return render_template('index.html', session_user_data=user_data)
    return render_template('index.html')

@bp.route('/onboarding')
@login_required
def onboarding():

    user_id = session['user_id']
    user_data = db.child('users').child(user_id).get().val()

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
                           session_user_data=user_data,
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
                    print("Username exists")
                    return jsonify({"message": "Username Exists", "exists": True}), 200
                else:
                    print("username is available")
                    return jsonify({"message": "username is available", "exists": False}), 200
        
            


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

        return jsonify({'message': 'Onboarding completed', 'redirect_url':url_for('profile.profile')})
    else:
        # Redirect to login if not logged in
        return redirect(url_for('authentication.login')) 
    
def my_quizzes(user_id):
    user_scores = db.child("users").child(user_id).child("scores").get().val()
    quizzes = db.child("users").child(user_id).child("quizzes").get().val()

    user_quiz_data = user_quizzes(db, user_id, quizzes)
    quiz_data = []

    for quiz in user_quiz_data:
        for quiz_id, quiz_info in quiz.items():
            quiz_category = quiz_info.get("category")
            quiz_difficulty = quiz_info.get("difficulty")
            quiz_title = quiz_info.get("quiz_title")
            quiz_answer_type = quiz_info.get("answer_type")
            quiz_type = quiz_info.get("quiz_type")
            question_count = quiz_info.get("question_count")
            score = quiz_info.get("score")

            quiz_data.append({
                quiz_id: {
                    "category": quiz_category,
                    "difficulty": quiz_difficulty,
                    "title": quiz_title,
                    "answer_type": quiz_answer_type,
                    "type": quiz_type,
                    "question_count": question_count,
                    "score": score
                }
            })
    
    return quiz_data

@bp.route("/<username>")
def profile(username):
    session_user_data = None
    username_data = None

    if 'user' in session and 'user_id' in session:

        user_id = session['user_id']
        session_user_data = db.child("users").child(user_id).get().val()
        print(session_user_data.get('username'))

        quiz_data = my_quizzes(user_id)
        print(quiz_data)

    # Fetch user data from Firebase using the username
    if username.lower() != "anonymous":
        username_data = db.child('users').order_by_child('username').equal_to(username).get().val()
        if username_data:
            user_id = list(username_data.keys())[0]  # This is the user_id
            username_data = list(username_data.values())[0]

            # Fetch quizzes if user_id is found
            if user_id:
                quiz_data = my_quizzes(user_id)
                
                user_score_data = db.child('users').child(user_id).child('scores').get().val()
                all_time_score = user_score_data.get('all_time_score')
                quiz_count, average_score = calculate_quiz_stats(user_score_data)

                # user created quizzes
                user_quizzes = db.child("users").child(user_id).child("quizzes").get().val()
                quizzes_created = len(user_quizzes)
                quiz_stats = {
                        'quiz_count': quiz_count,
                        'average_score': average_score,
                        'all_time_score': all_time_score,
                        'quizzes_created': quizzes_created
                    }

    # If no user data is found, return a 404 error
    if not username_data:
        flash("User not found. Redirecting to the homepage.", "error")  # Flash the error message
        return redirect(url_for('main.index'))  # Redirect to the main.index route
        
    if not username_data or not quiz_data:
        return redirect(url_for('main.index'))

    # Safe access to 'professional_info dictionary
    professional_info = username_data.get('professional_info', {})
    socials_data = username_data.get('socials', {})
    personal_info_fields = [
        ('Full name', username_data.get('name')),
                ('Email', username_data.get('email')),
                ('Phone', username_data.get('phone')),
                ('Gender', username_data.get('gender')),
                # Convert enthinicity list to a comma-separated string
                ('Ethnicity', ', '.join(username_data['ethnicity']) if isinstance(username_data.get('ethnicity'), list) else username_data.get('ethnicity')),
                ('dob', username_data.get('dob')),
                ('Address', username_data.get('address')),
                ('Country', username_data.get('country'))
            ]
    job_info_fields = [
        ('Industry', professional_info.get('industry')),
        ('Profession', professional_info.get('profession')),
        ('Seniority', professional_info.get('seniority')),
        ('Salary', professional_info.get('salary')),
        ('Education', professional_info.get('education'))
    ]
    socials = []
    if socials_data:
        socials = [
            ('website', socials_data.get('website')),
            ('github', socials_data.get('github')),
            ('facebook', socials_data.get('facebook')),
            ('twitter', socials_data.get('twitter')),
            ('instagram', socials_data.get('instagram'))
        ]

            # Filter out fields with None values
    personal_info_fields = [field for field in personal_info_fields if field[1] is not None]
    job_info_fields = [field for field in job_info_fields if field[1] is not None]

    return render_template('user_profile.html', 
                            session_user_data=session_user_data, 
                            user = username_data,
                            personal_info_fields=personal_info_fields, 
                            job_info_fields = job_info_fields,
                            socials = socials,
                            quiz_data= quiz_data,
                            quiz_stats = quiz_stats
                            )

        
@bp.route("/settings")
@login_required
def settings():
    user_id= session['user_id']
    user_data = db.child("users").child(user_id).get().val()
    
    return render_template('settings.html', session_user_data=user_data)

@bp.route("/edit_profile")
@login_required
def edit_profile():
    user_id = session['user_id']
    user_data = db.child('users').child(user_id).get().val()
    countries_raw = db.child("data").child("countries").get().val()
    countries = dict(sorted(countries_raw.items(), key=lambda item: item[1]))
    countries = sorted(countries.values())
    professional_info = user_data.get('professional_info', {})
    socials = []
    if user_data.get('socials', {}):
        socials = user_data.get('socials', {})
    professions = db.child("data").child("profession_data").child("professions").get().val()
    industries = db.child("data").child("profession_data").child("industries").get().val()
    education = db.child("data").child("profession_data").child("education").get().val()
    seniority = db.child("data").child("profession_data").child("seniority").get().val()
    salary = db.child("data").child("profession_data").child("salary range").get().val()
    return render_template('edit-profile.html', 
                           session_user_data= user_data, 
                           countries=countries, 
                           professional_info=professional_info,
                           socials = socials,
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
        social_fields = {'website', 'twitter', 'github', 'instagram', 'facebook'}
        for key, value in data.items():
            if key != 'user_id':
                if key in professional_info_fields:
                    db.child('users').child(user_id).child("professional_info").update({key: value})
                # If socials, update to socials
                elif key in social_fields:
                    db.child('users').child(user_id).child('socials').update({key: value})
                # If password, change to lowercase
                elif key == "username":
                    username = value.lower()
                    db.child('users').child(user_id).update({"username": username})
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
        return jsonify({'message': 'Profile photo uploaded successfuly', 'redirect_url': url} )
    return jsonify({'message': 'File upload falied'}), 500

