from flask import Flask, Blueprint, session, render_template, request, redirect, url_for, jsonify
import pyrebase

bp = Blueprint("main", __name__)

@bp.route("/")
def index():

    return render_template('home.html')

@bp.route('/onboarding')
def onboarding():
    if 'user' in session:
        user_email = session['user']

        return render_template('onboarding.html', user_email=user_email)
    else:
        return redirect(url_for('main.login'))  # Redirect to login if not logged in


@bp.route("/profile")
def profile():
    if 'user' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('authentication.login'))

@bp.route("/search")
def search():

    return render_template('search.html')

