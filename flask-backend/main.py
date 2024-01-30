from flask import Flask, Blueprint, session, render_template, request, redirect
import pyrebase

bp = Blueprint("main", __name__)

@bp.route("/")
def index():

    return render_template('login.html')


