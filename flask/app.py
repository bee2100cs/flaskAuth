from flask import Flask, session, render_template, request, redirect
import pyrebase
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask (__name__)

config = {
    'apiKey': os.environ.get("apiKey"),
    'authDomain': os.environ.get("authDomain"),
    'projectId': os.environ.get("projectId"),
    'storageBucket': os.environ.get("storageBucket"),
    'messagingSenderId': os.environ.get("messagingSenderId"),
    'appId': os.environ.get("appId"),
    'measurementId': os.environ.get("measurementId"),
    'databaseURL': ""
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()

app.secret_key = 'secret'

@app.route('/login', methods=['POST', 'GET'])
def login():
    if('user' in session):
        return 'Hi, {}'.format(session['user'])
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            session['user'] = email
            # Return greeting after login
            return 'Hi, {}'.format(session['user'])
        except:
            return 'Failed to login'
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('user')
    return redirect('/')

@app.route('/check_login')
def check_login():
    if 'user' in session:
        return 'Hi, {}'.format(session['user'])
    else:
        return 'Please log in'
    
if __name__ == '__main__':
    app.run(port=1111)

