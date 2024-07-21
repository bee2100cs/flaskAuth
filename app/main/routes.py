from . import main
from flask import render_template

@main.route("/")
def index():

    return render_template("home.html")

@main.route("/random-quiz")
def random_quiz():
    
    return render_template('random-quiz.html')