from . import main
from flask import Blueprint, render_template, redirect, request, session, url_for, g, jsonify
import json
from ..config import ApplicationConfig
from ..auth.authentication import login_required
from werkzeug.utils import secure_filename
from . import db
import random
import threading
import copy
from .utils.helper import (generate_question_id, 
                           fetch_data_from_api, 
                           fetch_session_token, 
                           get_key_by_value, 
                           add_questions_to_db,
                           save_quiz_to_db,
                           save_user_score,
                           normalize_text,
                           search_quizzes,
                           get_quiz_data_by_id,
                           questions_without_correct_answers,
                           get_quiz_question_ids,
                           user_quizzes,
                           calculate_quiz_stats
                           )

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
     # Get categories
    categories = db.child("quiz").child("categories").child("trivia_api").get().val()
    return render_template('existing-quiz.html', session_user_data=g.user_data, categories=categories)




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

                # Data to send to front-end
                answers = question['incorrect_answers'] + [question['correct_answer']]

                random.shuffle(answers)

                if question['type'] == 'boolean':
                    answers = ['True', 'False']
                # Data to save in database
                questions_with_id.append({
                    'id': question_id,
                    'type': question['type'],
                    'difficulty': question['difficulty'],
                    'category': question['category'],
                    'question': question['question'],
                    'answers': answers,
                    'correct_answer': question['correct_answer']
                })

                questions_only.append({
                    'id': question_id,
                    'question': question['question'],
                    'answers': answers
                })

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

# Route to search existing quiz data
@main.route('/search-quizzes', methods=['POST','GET'])
def search_quizzes_route():
    data = request.json
    quiz_category = data.get('quiz_category', 'random')
    answer_type = data.get('answer_type', 'random')
    quiz_difficulty = data.get('quiz_difficulty', 'random')

    quizzes = search_quizzes(db, quiz_category, answer_type, quiz_difficulty)
    
    if quizzes is not None:
        session_quizzes_data = []
        for quiz in quizzes:
            session_quizzes_data.append(quiz)
            user_id = quiz['quiz_data']['user_id']
            user_data = db.child('users').child(user_id).get().val()
            username = user_data['username']
            quiz['username'] = username

            del quiz['quiz_data']['questions']
            

        session['quizzes'] = quizzes
        return jsonify({"quizzes": quizzes}), 200
    else:
        return jsonify({"error": "An error occurred while searching for quizzes"}), 500

@main.route("/get-existing", methods=['POST'])
def get_existing():
    try:
        quiz_id = request.json['quiz_id']
        
        question_ids = get_quiz_question_ids(quiz_id)

        # Get questions from db
        quiz_question_data = get_quiz_data_by_id(db, question_ids)
        
        session['quiz_questions'] = copy.deepcopy(quiz_question_data)

        # Questions without answers for frontend
        questions_only = questions_without_correct_answers(copy.deepcopy(quiz_question_data))
        question_count = len(questions_only)
        session['total_questions'] = question_count
        session['quiz_id'] = quiz_id
        saved_quiz_id = session.get("quiz_id")
        print(saved_quiz_id)

        quizzes = session.get('quizzes', [])
        for quiz in quizzes:
            if quiz['quiz_id'] == quiz_id:
                quiz_type = quiz['quiz_data'].get('quiz_type')

        return jsonify({
            'message': 'Questions sent to front-end',
            'quiz_questions': questions_only,
            'question_count': question_count,
            'quiz_type': quiz_type}), 200
    except Exception as e:
        return jsonify({"error": "Failed to fetch quiz data"})


@main.route("/quiz")
def quiz():
      
    return render_template("quiz.html", session_user_data=g.user_data)

@main.route("/quiz", methods=["POST", "GET"])
def quiz_callback():
    
    if 'quiz_questions' in session:
        quiz_questions = session.get('quiz_questions')
        print("session quiz uestions",quiz_questions)
        total_questions = int(session.get("total_questions"))
    else:
        return({"messsage": "No questions found in session"})
    
    #process quiz answers
    user_answers= request.json.get('answers')
    print('user answers:', user_answers)
    score = 0
    review_data = []

    #print("correct answer:", correct_answers)
    for question in quiz_questions:
        question_id = question['id']
        correct_answer = question['correct_answer']
        user_answer = user_answers.get(question_id)
        print(F'question_id{question_id}, correct naswer{correct_answer}, user-answer{user_answer}')

        # Track the review data
        review_data.append({
            'question': normalize_text(question['question']),
            'correct_answer': normalize_text(correct_answer),
            'user_answer': normalize_text(user_answer) if user_answer else None,
            'is_correct': user_answer == correct_answer if user_answer else False
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
    
    return render_template("results.html", review_data=review_data, session_user_data=g.user_data)
    
@main.route('/save-quiz', methods=['POST','GET'])
def save_quiz():

    try:
        quiz_questions = session.get('quiz_questions')
        quiz_id = session.get("quiz_id")
        user_id = session.get("user_id")
        score = request.json.get('score')  # Get score from the request

        # If quiz_id not in session, save quiz and get quiz_id
        print("heres the quiz_id", quiz_id)
        if not quiz_id:
            quiz_id = save_quiz_to_db(session, quiz_questions)
            session['quiz_id'] = quiz_id
        
        if quiz_id and user_id:
            save_user_score(quiz_id, session, score)
            
            # Clear session data
            session.pop('quiz_questions', None)
            session.pop('numberOfQuestions', None)
            session.pop('quiz_id', None)

            return jsonify({"redirect_url": url_for("main.index"), "message": "Quiz saved successfully"})
        else:
            return jsonify({"redirect_url": url_for("main.index"), "message": "Quiz saved successfully for anonymous"})
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
    print("search function called")
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


@main.route('/my_quizzes')
def my_quizzes():
    if 'user_id' in session:
       
        user_id = session['user_id']
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

                quiz_data.append(
                    {quiz_id: {
                        "category": quiz_category,
                        "difficulty": quiz_difficulty,
                        "title": quiz_title,
                        "answer_type": quiz_answer_type,
                        "type": quiz_type,
                        "question_count": question_count,
                        "score": score
                }})

        return render_template("my_quizzes.html",
                               quiz_data=quiz_data, 
                                session_user_data=g.user_data)
    
    else:
        return redirect(url_for('main.index'))
    

@main.route('/quiz_stats')
def quiz_stats():
    if 'user_id' in session:
        user_id = session.get("user_id")
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

        return render_template('quiz_stats.html',
                               quiz_stats= quiz_stats,
                           session_user_data=g.user_data)
    else:
        return redirect(url_for('main.index'))