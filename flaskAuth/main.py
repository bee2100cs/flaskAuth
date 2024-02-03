from flask import Flask, Blueprint, session, render_template, request, redirect, url_for
import pyrebase

bp = Blueprint("main", __name__)

@bp.route("/")
def index():

    return render_template('firebase.html')

@bp.route('/welcome')
def welcome():
    if 'user' in session:
        user_email = session['user']
        return render_template('welcome.html', user_email=user_email)
    else:
        return redirect(url_for('main.index'))  # Redirect to login if not logged in


@bp.route("/home")
def home():

    return "You are all logged in"

