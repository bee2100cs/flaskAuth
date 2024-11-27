import hashlib
import requests
from .. import db
import uuid
from flask import jsonify
from datetime import datetime, timezone
import unicodedata
import html
import random

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
    full_question_Id = hashlib.sha256(question_text.encode('utf-8')).hexdigest()
    trancated_question_id = full_question_Id[:13]
    return trancated_question_id


def normalize_text(text):
    return unicodedata.normalize('NFKD', html.unescape(text).strip().lower())

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
    full_user_Id = hashlib.sha256(username.encode('utf-8')).hexdigest()
    trancated_user_id = full_user_Id[:28]
    return trancated_user_id

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
    quiz_id = session.get("quiz_id")
    if not quiz_id:
        try:
            if 'user_id' in session:
                user_id = session['user_id']
                print(f"Logged in user ID: {user_id}")
            else:
                user_id = get_or_create_anonymous_user()
                print(f"Anonymous user ID: {user_id}")
            
            try:
                # Generate a unique quiz ID
                quiz_id_raw = str(uuid.uuid4())
                hashed_id = hashlib.sha256(quiz_id_raw.encode('utf-8')).hexdigest()
                quiz_id_truncated = hashed_id[:8]
                quiz_id = quiz_id=f"quiz_{quiz_id_truncated}"
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
            question_types = set()
            
            for question in quiz_questions:
                # Get question types, categories, and difficulties
                difficulties.add(question.get('difficulty'))
                categories.add(question.get('category'))
                question_types.add(question.get('type'))

            def determine_value(values_set):
                if len(values_set) == 1:
                    return next(iter(values_set))
                elif len (values_set) > 1:
                    return 'random'
                else:
                    return None
                
            quiz_category = determine_value(categories)
            quiz_difficulty = determine_value(difficulties)
            quiz_question_type = determine_value(question_types)
            
            # Determine the quiz type based on conditions
            if quiz_category != 'random' or quiz_difficulty != 'random' or quiz_question_type != 'random':
                quiz_type = 'custom'
            else:
                quiz_type = 'random'

            quiz_title = f"{quiz_type} {quiz_id}"
            # prepare quiz data
            quiz_data = {
                "user_id": user_id,
                "quiz_title": quiz_title,
                'category': quiz_category,
                'answer_type' : quiz_question_type,
                'quiz_type' : quiz_type,
                'difficulty': quiz_difficulty,
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
    try:
        # Prepare the score data
        score_data = {
            "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        all_time_score = 0
        # Fetch the user's existing scores for the quiz
        user_scores = db.child("users").child(user_id).child("scores").child(quiz_id).get().val()
        all_time_score = db.child('users').child(user_id).child('scores').child("all_time_score").get().val()
        if user_scores:
            # If the user has already taken the quiz, update the score if the new score is higher
            if int(score) > int(user_scores.get('score', 0)):
                db.child("users").child(user_id).child("scores").child(quiz_id).update(score_data)
                print(f"Updated score for user {user_id} for quiz {quiz_id}")
            else:
                print(f"New score is not higher. Score for user {user_id} for quiz {quiz_id} remains unchanged.")
        else:
            # Save the new score
            db.child("users").child(user_id).child("scores").child(quiz_id).set(score_data)
            print(f"Score saved successfully for user {user_id} and quiz {quiz_id}")

            if all_time_score:
                # Add current score to all_time_score
                all_time_score = int(all_time_score) + int(score)
            else:
                # Add new all_time_score
                all_time_score = score
            db.child('users').child(user_id).child('scores').child('all_time_score').set(all_time_score)
    except Exception as e:
        print(f"Error saving user score: {e}")
        return jsonify({"error": "An error occurred while saving the user score"})
    

# Quiz search function
def search_quizzes(db, quiz_category='random', quiz_question_type='random', quiz_difficulty='random'):
    try:
        quizzes_ref = db.child("quiz").child("saved_quizzes").get()
        matching_quizzes = []

        for quiz_data in quizzes_ref.each():
            quiz_info = quiz_data.val()
            
            if (quiz_category == 'random' or quiz_info['category'] == quiz_category) and \
                (quiz_question_type == 'random' or quiz_info['answer_type'] == quiz_question_type) and \
                (quiz_difficulty == 'random' or quiz_info['difficulty'] == quiz_difficulty):
                matching_quizzes.append({
                    'quiz_id': quiz_data.key(),
                    'quiz_data': quiz_info
                })
        
        return matching_quizzes
            
    except Exception as e:
        print(f"Error searching quizzes: {e}")
        return None

def user_quizzes(db, user_id, quizzes):
    try:

        # Ensure quizzes is a valid iterable, defaulting to an empty list
        if quizzes is None:
            return []
        
        user_quizzes = []
        # Loop thorugh quizzes created by user
        for quiz_id in quizzes:
            quiz_data = db.child("quiz").child("saved_quizzes").child(quiz_id).get().val()
            quiz_score = db.child("users").child(user_id).child("scores").child(quiz_id).child("score").get().val()
            
            if quiz_data:  # Ensure that quiz_data exists
                quiz_data['score'] = quiz_score if quiz_score else 0

                user_quizzes.append({quiz_id: quiz_data})
            

        return user_quizzes

    except Exception as e:
        print(f"Error in user_quiz: {e}")
        return user_quizzes
    
# Get quiz question IDs
def get_quiz_question_ids(quiz_id):
    question_ids = db.child('quiz').child('saved_quizzes').child(quiz_id).child('questions').get().val()
    return question_ids
# Get featured quizzes
def get_quiz_data_by_id(db, question_ids):
    questions = []
    for question_id in question_ids:
        question_data = db.child('quiz').child('questions').child(question_id).get().val()
        id = question_id
        question = question_data['question']
        answers = question_data['answers']
        correct_answer = question_data['correct_answer']

        questions.append({
            'id': id,
            'question': question,
            'answers': answers,
            'correct_answer': correct_answer
        })

    #print('theseare the questions',questions)
    return questions

def questions_without_correct_answers(questions):
    
    for question in questions:
        if 'correct_answer' in question:
            del question['correct_answer']

    return questions

# User quiz stats
def calculate_quiz_stats(data):
    quiz_count = 0
    all_time_score = int(data.get("all_time_score"))

    for key, value in data.items():
        if key != 'all_time_score':
            score = int(value['score'])
            quiz_count += 1
    
    #  Calculate the average score if there are any quizzes
    if quiz_count > 0:
        average_score = round(all_time_score / quiz_count)
    else:
        average_score = 0

    return quiz_count, average_score

# Get other quizzes not created by user but taken by user
def quizzes_by_other_users(user_scores, user_quiz_ids):
    quizzes_by_others = []

    try:
        if not user_scores:
            print("No user scores found.")
            return quizzes_by_others  # Return an empty list if no scores
        
        for quiz_id, value in user_scores.items():
            if quiz_id == 'all_time_score' or quiz_id in user_quiz_ids:
                continue

            quiz_score = int(value['score'])
            quiz_id = quiz_id
            quiz_data = db.child("quiz").child("saved_quizzes").child(quiz_id).get().val()
            if quiz_data:  # Ensure that quiz_data exists
                user_id = quiz_data['user_id']
                user_data = db.child('users').child(user_id).get().val()
                username = user_data['username']
                print("username is: ", username)
                quiz_data['score'] = quiz_score if quiz_score else 0
                quiz_data['username'] = username
                quizzes_by_others.append(
                    {quiz_id: quiz_data}
                )
            else:
                print(f"Quiz data for quiz_id {quiz_id} does not exist.")

        return quizzes_by_others
    except Exception as e:
        print(f"Error in quizzes_by_other_users: {e}")
        return quizzes_by_others

    

