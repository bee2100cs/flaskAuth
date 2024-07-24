from config import ApplicationConfig
import pyrebase
import json
from flask import jsonify
import requests

### Run python3 populate-data.py on terminal to 
# populate countries and professions data on the firebase realtime database

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# # #Store country json data to file
# try:

#     with open("static/data/countries.json", "r") as file:
#         data = json.load(file)

# except Exception as e:
#     print("Error reading data")


# #Simplify the data
# simplified_data = {country['code']: country['name'] for country in data['countries']}
# db.child("data").child("countries").set(simplified_data)
# print("data added to firebase database")

# # Store professions json data to file
# with open("static/data/professions.json", 'r') as file:
#     profession_data = json.load(file)
    
# db.child("data").child("profession_data").update(profession_data)
# print("data updated")


# profession_data = db.child("data").child("professions").get().val()

# print (profession_data)


# # Add trivia categories
# # API to get questions from TRIVIA API
# def fetch_data_from_api(api_url):
#     response = requests.get(api_url)
#     response.raise_for_status()
#     return response.json()

# api_url = 'https://opentdb.com/api_category.php'
# data = fetch_data_from_api(api_url)

# categories_list = data['trivia_categories']
# categories_dict = {category['name']: category['id'] for category in categories_list}

# db.child("quiz").child("categories").child('trivia_api').set(categories_dict)

# trivia_categories = db.child("quiz").child("categories").child("trivia_api").get().val()
# sorted_dict = dict(sorted(trivia_categories.items(), key=lambda item: item[1]))
# print(sorted_dict)

# # Function to get category Id from DB
# def get_key_by_value(data_dict, target_value):
#     for key, value in data_dict.items():
#         if key == target_value:
#             return value
#     return None

# category = 'Animals'
# category_id = get_key_by_value(trivia_categories, category)
# print(category_id)