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
    'databaseURL': ""
}
firebase = pyrebase.initialize_app(config)

storage = firebase.storage()

# Upload file to firebase cloud
# filename=input("enter the name of the file you want to upload: ")
# cloudfilename=input("enter the file on the cloud: ")
# storage.child(cloudfilename).put(filename)


# Download file from firebase cloud
# cloudfilename=input("Enter file to download: ")
# storage.child(cloudfilename).download("","downloaded.txt")

# Reading file
cloudfilename=input("enter the file on the cloud: ")
url = storage.child(cloudfilename).get_url(None)

f=urllib.request.urlopen(url).read()
print(f)

