from flask import Blueprint, session, jsonify, render_template, request, redirect, url_for, flash
from config import ApplicationConfig
import pyrebase
import json

#bp = Blueprint("authentication", __name__)

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

db = firebase.database()
# # Create
# data={'age':32, 'address':"Texas", 'employed':True, 'name':'Eddy Mwalimu'}
# #db.child("users").child("user").push(data)
# #db.child("users").child("user").set(data)

# #update
# db.child("users").child("user").update({'name':'Job'})


# #Store country json data to file
# with open("countries.json", "r") as file:
#     data = json.load(file)

# #Simplify the data
# simplified_data = {country['code']: country['name'] for country in data['countries']}
# db.child("data").child("countries").set(simplified_data)
# print("data added to firebase database")

# # Store professions json data to file
# with open("professions.json", 'r') as file:
#     profession_data = json.load(file)
    
# db.child("data").child("profession_data").update(profession_data)
# print("data updated")


#profession_data = db.child("data").child("professions").get().val()

#print (profession_data)