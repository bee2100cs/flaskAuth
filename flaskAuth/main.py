from flask import Flask, Blueprint, session, render_template, request, redirect, url_for, jsonify
import pyrebase

bp = Blueprint("main", __name__)

@bp.route("/")
def index():

    return render_template('login.html')

@bp.route('/onboarding')
def onboarding():
    if 'user' in session:
        user_email = session['user']

        return render_template('onboarding.html', user_email=user_email)
    else:
        return redirect(url_for('main.index'))  # Redirect to login if not logged in


@bp.route("/home")
def home():

    return "You are all logged in"