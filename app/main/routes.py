from . import main
from flask import Blueprint, render_template, redirect, request, session, url_for, g, jsonify
import json
from ..config import ApplicationConfig
from ..auth.authentication import login_required
from werkzeug.utils import secure_filename
from . import db
from utils.helper import generate_question_id, fetch_data_from_api, fetch_session_token, get_key_by_value

# Global variables
session_token = None


@main.route('/')
def index():

    return render_template('index.html', session_user_data=g.user_data)

@main.route("/random-quiz")
def random_quiz():

    return render_template('random-quiz.html', session_user_data=g.user_data)

@main.route("/custom-quiz")
def custom_quiz():

    return render_template('custom-quiz.html', session_user_data=g.user_data)

@main.route("/existing-quiz")
def existing_quiz():

    return render_template('existing-quiz.html', session_user_data=g.user_data)




@main.route("/api/quiz", methods=["POST", 'GET'])
def create_quiz():
    global session_token

    if session_token is None:
        fetch_session_token()
        
    data = request.get_json()
    number_of_questions = data.get('question_count', 10)
    category = data.get('quiz_category', None)
    difficulty = data.get('quiz_difficulty', None)
    quiz_type = data.get('quiz_type', None)

    # Get category ID from firebase DB
    # Get category data
    category_data = db.child("quiz").child('categories').child('trivia_api').get().val()
    category_id = get_key_by_value(category_data, category)

    api_url = 'https://opentdb.com/api.php?'

    api_url += f'amount={number_of_questions}'

    if category:
        api_url += f'&category={category_id}'
    if difficulty in ['easy', 'medium', 'hard']:
        api_url += f'&difficulty={difficulty}'
    if quiz_type in ['multipe', 'boolean']:
        api_url += f'&type={quiz_type}'

    print(api_url)

    try:
        quiz_data = fetch_data_from_api(api_url)
        response_code = quiz_data.get("response_code")
        if response_code == 0:
            # Sucess, returned results successfully
            results = quiz_data.get("results", [])

            session['quiz_questions'] = results
            return jsonify({'redirect_url': url_for('main.quiz'),  'message': 'success'})
        
        # If error
        elif response_code == 1:
            # No resutls, the API doesnt have enough questions for your querry
            print("Error: No results. The API doesn't have enough questions for your query.")
            return jsonify({"message": "No results"}),401
        elif response_code == 2:
            # Invalid parameter
            print("Error: Invalid parameters.")
            return jsonify({"message": "Invalid parameters"}), 400
        elif response_code == 3:
            # Token not found
            print("Error: Token not found.")
            return jsonify({"message": "Token not found"}), 404
        elif response_code == 4:
            # Token empty- returned all possible questions
            print("Error: Token empty - returned all possible questions.")
            return jsonify({"message": "Token empty"}), 401
        elif response_code == 5:
            # Rate limit
            print("Error: Rate limit exceeded.")
            return jsonify({"message": "Rate limit"}), 429
        else:
            print(f"Error: Unexpected response code {response_code}")
            return jsonify({"message": "Unexpected response code"}), 500
    except Exception as e:
        return jsonify({"message": str(e)}), 500



@main.route("/quiz")
def quiz():
    if 'quiz_questions' in session:
        quiz_questions = session['quiz_questions']
        print ("Here are questions served from current session")

        # Add unique ID to questions
        questions_only = []
        questions_with_id = []
        for question in quiz_questions:
            question_id = generate_question_id(question['question'])

            # Data to save in database
            questions_with_id.append({
                'id': question_id,
                'type': question['type'],
                'difficulty': question['difficulty'],
                'category': question['category'],
                'question': question['question'],
                'answers': question['incorrect_answers'] + [question['correct_answer']]
            })
            # Data to send to front-end
            answers = question['incorrect_answers'] + [question['correct_answer']]

            if question['type'] == 'boolean':
                answers = ['True', 'False']
            questions_only.append({
                'id': question_id,
                'question': question['question'],
                'answers': answers
            })

        # Shuffle the answers for each question
        import random 
        for q in questions_only:
            random.shuffle(q['answers'])

        # Store questions with ids in session for answer validation and sending to db
        session["quiz_questions"] = questions_with_id

        # Render quiz page with questions
        return render_template("quiz.html", session_user_data=g.user_data, quiz_data=questions_only)
    else:
        print('Oops! Something broke: No questions found in session')
        return render_template("error.html", session_user_data=g.user_data)

@main.route("/quiz", methods=["POST", "GET"])
def quiz_callback():
    #process quiz answers
    user_answers= request.json.get('answers')
    quiz_questions = session.get('quiz_questions')

    if not quiz_questions:
        return({"messsage": "No questions found in session"})
    
    score = 0
    total_questions = len(quiz_questions)
    for question in quiz_questions:
        q_text = question['question']
        correct_answer = question['correct_answer']
        user_answer = user_answer.get(q_text)

        if user_answer == correct_answer:
            score += 1
    
    # Calculate percentage score
    percentage_score = (score / total_questions) * 100
    
    return jsonify({"message": "quiz completed", 'score': score, 'percentage_score': percentage_score})