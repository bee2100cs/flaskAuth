import hashlib
import requests
from .. import db
import uuid
from flask import jsonify
from datetime import datetime, timezone


# Generate session token from Trivia API
#  to keep track of questions the API has already retrieved.
def fetch_session_token():
    global session_token
    response_code = None
    response = requests.get('https://opentdb.com/api_token.php?command=request')
    data = response.json()
    session_token = data.get('token')
    return session_token

# Function to fetch data from Trivia API
def fetch_data_from_api(api_url):
    global session_token
    response = requests.get(f'{api_url}&token={session_token}')
    response.raise_for_status()
    data = response.json()
    if data.get('response_code') in (4, 3):
        # Generate new token
        session_token = fetch_session_token()
        response = requests.get(f'{api_url}&token={session_token}')
    return data

# Function to get category Id from DB
def get_key_by_value(data_dict, target_value):
    for key, value in data_dict.items():
        if key == target_value:
            return value
    return None


# Function to Generate a unique ID based on the string of the question 
# using hashing function
# so that the same question will always generate the same unique ID
# ensuring that no duplicate questions are added to the database
def generate_question_id(question_text):
    return hashlib.sha256(question_text.encode('utf-8')).hexdigest()


# Add generated questions to our db
def add_question_to_db(question):
    if not isinstance(question, dict):
        raise ValueError("Expected 'question' to be a dictionary")
    question_id = question['id']

    # Check if question ID already exists in the db
    existing_question = db.child("quiz").child("questions").child(question_id).get().val()

    if existing_question:
        print(f"Question with ID{question_id} already exists.")
        return False
    else:
        # Add the question to db
        db.child("quiz").child("questions").child(question_id).set(question)
        print(f"Question added sucessfully.")
        return True

# Add all quiz questions to db
def add_questions_to_db(questions):
    for question in questions:
        add_question_to_db(question)


# Create anonymous user
def generate_user_id(username):
    return hashlib.sha256(username.encode('utf-8')).hexdigest()

def get_or_create_anonymous_user():
    anonymous_username = 'anonymous'
    anonymous_user_id = generate_user_id(anonymous_username)
    # Check if anonymous user exists
    existing_user = db.child("users").child(anonymous_user_id).get().val()
    if not existing_user:
        db.child('users').child(anonymous_user_id).set({"username": anonymous_username})
    return anonymous_user_id


# Save quiz to db
def save_quiz_to_db(session, quiz_questions):
    
    # Check if there's quiz data in session
    if not quiz_questions:
        print("No quiz data to save")
        return
    # Check if user is logged in or is anonymous
    try:
        if 'user_id' in session:
            user_id = session['user_id']
            print(f"Logged in user ID: {user_id}")
        else:
            user_id = get_or_create_anonymous_user()
            print(f"Anonymous user ID: {user_id}")
        
        try:
            # Generate a unique quiz ID
            quiz_id = str(uuid.uuid4())
            print(f"Generated unique quiz_id {quiz_id}")
        except Exception as e:
            print("error generating quiz_id")
            jsonify({"error": " an error occured when creating quiz_id"})

        # Extract question IDs
        question_ids = [question['id'] for question in quiz_questions]
        number_of_questions = len(question_ids)

        # Get other quiz parameters
        # use sets to avoid data duplication
        difficulties = set()
        categories = set()
        types = set()
        
        for question in quiz_questions:
            # Get question types, categories, and difficulties
            difficulties.add(question.get('difficulty'))
            categories.add(question.get('category'))
            types.add(question.get('type'))

        def determine_value(values_set):
            if len(values_set) == 1:
                return next(iter(values_set))
            elif len (values_set) > 1:
                return 'random'
            else:
                return None
            
        quiz_category = determine_value(categories)
        quiz_difficulty = determine_value(difficulties)
        quiz_type = determine_value(types)

        print(f"Quiz category: {quiz_category}, quiz difficulty: {quiz_difficulty}, quiz type: {quiz_type}")

        # prepare quiz data
        quiz_data = {
            "user_id": user_id,
            'quiz_category': quiz_category,
            'quiz_type' : quiz_type,
            'quiz_difficulty': quiz_difficulty,
            'question_count': number_of_questions,
            "questions": question_ids
        }
        # Save quiz to db
        try:
            db.child("quiz").child("saved_quizzes").child(quiz_id).set(quiz_data)

            print(f"Quiz saved with ID {quiz_id} fo user {user_id}")
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return jsonify({"error": "An error occured while saving the quiz"})
        
        # Append quiz ID to list of quizzes by user on db
        try:
            user_quizzes = db.child("users").child(user_id).child("quizzes").get().val()
            if not user_quizzes:
                user_quizzes = [quiz_id]
                
            else:
                user_quizzes.append(quiz_id)

            db.child("users").child(user_id).child("quizzes").set(user_quizzes)
            print("quiz saved successfully")
        except Exception as e:
            print(f"Unexpected error: {e}")
            return jsonify({"Error": "An unexpected error occured"})

        return quiz_id
    
            
    except Exception as e:
        print(f"error handling user_id. Error: {e}")
        return jsonify({"error": "An error occured during handling user_id "})

def save_user_score(quiz_id, session, score):
    if 'user_id' in session:
            user_id = session['user_id']
    else:
        user_id = get_or_create_anonymous_user()
    try:
        # Prepare the score data
        score_data = {
            "quiz_id": quiz_id,
            "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        # Fetch the user's existing scores for the quiz
        user_scores = db.child("users").child(user_id).child("scores").child(quiz_id).get().val()
        
        if user_scores:
            # If the user has already taken the quiz, update the score if the new score is higher
            if score > user_scores.get('score', 0):
                db.child("users").child(user_id).child("scores").child(quiz_id).update(score_data)
                print(f"Updated score for user {user_id} for quiz {quiz_id}")
            else:
                print(f"New score is not higher. Score for user {user_id} for quiz {quiz_id} remains unchanged.")
        else:
            # Save the new score
            db.child("users").child(user_id).child("scores").child(quiz_id).set(score_data)
            print(f"Score saved successfully for user {user_id} and quiz {quiz_id}")
    except Exception as e:
        print(f"Error saving user score: {e}")
        return jsonify({"error": "An error occurred while saving the user score"})