import pyrebase
import urllib
import os
from dotenv import load_dotenv
from flask import Blueprint, session, render_template, request, redirect, url_for
#from . import firebase
load_dotenv()

#bp = Blueprint("authentication", __name__)

config = {
    'apiKey': os.environ.get("apiKey"),
    'authDomain': os.environ.get("authDomain"),
    'projectId': os.environ.get("projectId"),
    'storageBucket': os.environ.get("storageBucket"),
    'messagingSenderId': os.environ.get("messagingSenderId"),
    'appId': os.environ.get("appId"),
    'measurementId': os.environ.get("measurementId"),
    'databaseURL': "database_url"
}
firebase = pyrebase.initialize_app(config)

db = firebase.database()
# Create
data={'age':32, 'address':"Texas", 'employed':True, 'name':'Eddy Mwalimu'}
#db.child("users").child("user").push(data)
#db.child("users").child("user").set(data)

#update
db.child("users").child("user").update({'name':'Job'})




