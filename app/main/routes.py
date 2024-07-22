from . import main
from flask import Blueprint, render_template, redirect, session, url_for
from ..config import ApplicationConfig
from ..auth.authentication import login_required
from werkzeug.utils import secure_filename


@main.route("/")
def index():
    if 'user' in session and 'user_id' in session:
        user_data = session.get('user_data')
        return render_template('home.html', session_user_data=user_data)
    return render_template('home.html')

@main.route("/random-quiz")
def random_quiz():
    
    return render_template('random-quiz.html')