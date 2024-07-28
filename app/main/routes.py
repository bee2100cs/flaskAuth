from . import main
from flask import Blueprint, render_template, redirect, request, session, url_for, g, jsonify
import json
from ..config import ApplicationConfig
from ..auth.authentication import login_required
from werkzeug.utils import secure_filename
from . import db
import random
import threading
from .utils.helper import (generate_question_id, 
                           fetch_data_from_api, 
                           fetch_session_token, 
                           get_key_by_value, 
                           add_questions_to_db,
                           save_quiz_to_db,
                           save_user_score,
                           normalize_text)

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

    # Get categories
    categories = db.child("quiz").child("categories").child("trivia_api").get().val()
    return render_template('custom-quiz.html', session_user_data=g.user_data, categories=categories)

@main.route("/existing-quiz")
def existing_quiz():

    return render_template('existing-quiz.html', session_user_data=g.user_data)




@main.route("/api/quiz", methods=["POST", 'GET'])
def create_quiz():
    global session_token

    if session_token is None:
        fetch_session_token()
        
    data = request.get_json()
    number_of_questions = data.get('question_count', 5)
    category = data.get('quiz_category', None)
    difficulty = data.get('quiz_difficulty', None)
    answer_type = data.get('answer_type', None)

    # Get category ID from firebase DB
    # Get category data
    
    category_data = db.child("quiz").child('categories').child('trivia_api').get().val()
    category_id = get_key_by_value(category_data, category)

    api_url = 'https://opentdb.com/api.php?'

    api_url += f'amount={number_of_questions}'

    if category_id is not None:
        api_url += f'&category={category_id}'
    if difficulty in ['easy', 'medium', 'hard']:
        api_url += f'&difficulty={difficulty}'
    if answer_type in ['multiple', 'boolean']:
        api_url += f'&type={answer_type}'

    try:
        print(f"Category:{category_id}, difficulty: {difficulty}, answer_type: {answer_type}")
        print(f"api_url: {api_url}")
        quiz_data = fetch_data_from_api(api_url)
        response_code = quiz_data.get("response_code")
        if response_code == 0:
            # Sucess, returned results successfully
            quiz_questions = quiz_data.get("results", [])

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
                    'incorrect_answers': question['incorrect_answers'],
                    'correct_answer': question['correct_answer']
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
            for q in questions_only:
                random.shuffle(q['answers'])

            # Store questions with ids in session for answer validation and sending to db
            session["quiz_questions"] = questions_with_id
            session['questions'] = questions_only
            quiz_questions = session['quiz_questions']
            session['total_questions'] = number_of_questions

            # Cread and start a thread to handle the slow database operation asynchronously
            db_thread = threading.Thread(target=add_questions_to_db, args=(quiz_questions,))
            db_thread.start()


            return jsonify({'redirect_url': url_for('main.quiz'), 
                            'message': 'success',
                            'total_questions': number_of_questions, 
                            "quiz_questions": questions_only})
        
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
    if 'questions' in session:
        questions = session['questions']
        total_questions = session['total_questions']
        return render_template("quiz.html", session_user_data=g.user_data, questions=questions, total_questions= total_questions)
   

@main.route("/quiz", methods=["POST", "GET"])
def quiz_callback():
    
    if 'quiz_questions' in session:
        quiz_questions = session.get('quiz_questions')
        total_questions = int(session.get("total_questions"))
    else:
        return({"messsage": "No questions found in session"})
    
    #process quiz answers
    user_answers= request.json.get('answers')
    print('user answers:', user_answers)
    score = 0

    # Create a dictionary for quick lookup of correct answers by ID
    correct_answers = {q['id']: q['correct_answer'] for q in quiz_questions}
    review_data = []
    #print("correct answer:", correct_answers)
    for question in quiz_questions:
        question_id = question['id']
        correct_answer = correct_answers.get(question_id)
        user_answer = user_answers.get(question_id)

        # Track the review data
        review_data.append({
            'question': normalize_text(question['question']),
            'correct_answer': normalize_text(correct_answer),
            'user_answer': normalize_text(user_answer),
            'is_correct': user_answer == correct_answer
        })

        if user_answer == correct_answer:
            score += 1
    session['review_data'] = review_data
    print(review_data)
    
    # Calculate percentage score
    percentage_score = round((score / total_questions) * 100)
    print("User score:", score, percentage_score)
    return jsonify({"redirect_url": url_for('main.results'), "message": "success", 'score': score, 'percentage_score': percentage_score})

@main.route("/results", methods=['POST', 'GET'])
def results():
    review_data = session['review_data']
    
    return render_template("results.html", review_data=review_data)
    
@main.route('/save-quiz', methods=['POST','GET'])
def save_quiz():

    try:
        quiz_questions = session.get('quiz_questions')
        score = request.json.get('score')  # Get score from the request

        # Save quiz and get quiz_id
        quiz_id = save_quiz_to_db(session, quiz_questions)
        
        if quiz_id:
            save_user_score(quiz_id, session, score)
            
            # Clear session data
            session.pop('quiz_questions', None)
            session.pop('numberOfQuestions', None)


            return jsonify({"redirect_url": url_for("main.index"), "message": "Quiz saved successfully"})
        else:
            return jsonify({"error": "Failed to save quiz"}), 500
    except Exception as e:
        print(f"Error finishing quiz: {e}")
        return jsonify({"error": "Failed to finish quiz"}), 500

# Handle the pending data before redirecting to login
@main.route('/save-pending-quiz', methods=['POST'])
def save_pending_quiz():
    try:
        score = request.json.get('score')
        quiz_questions = session.get('quiz_questions')
        if not quiz_questions:
            return jsonify({"error": "No quiz data to save"}), 400

        session['pending_quiz_data'] = {
            'quiz_questions': quiz_questions,
            'score': score
        }
        session['next_url'] = url_for('main.handle_pending_quiz')
        return jsonify({"redirect_url": url_for('authentication.login')})
    except Exception as e:
        print(f"Error saving pending quiz data: {e}")
        return jsonify({"error": "Failed to save pending quiz data"}), 500

# Route to handle pending quiz data after login
@main.route('/handle-pending-quiz', methods=['GET'])
def handle_pending_quiz():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({"error": "User not logged in"}), 401

        pending_quiz_data = session.get('pending_quiz_data')
        if not pending_quiz_data:
            return jsonify({"error": "No pending quiz data"}), 400

        quiz_questions = pending_quiz_data['quiz_questions']
        score = pending_quiz_data['score']

        quiz_id = save_quiz_to_db(session, quiz_questions)
        save_user_score(quiz_id, session, score)

        # Clear pending data from the session
        session.pop('pending_quiz_data', None)

        return redirect(url_for('main.index'))
    except Exception as e:
        print(f"Error handling pending quiz data: {e}")
        return jsonify({"error": "Failed to handle pending quiz data"}), 500

