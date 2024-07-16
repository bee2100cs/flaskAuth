from config import ApplicationConfig
import pyrebase
import json

### Run python3 populate-data.py on terminal to 
# populate countries and professions data on the firebase realtime database

#firebase config
config = ApplicationConfig.FIREBASE_CONFIG

firebase = pyrebase.initialize_app(config)

db = firebase.database()

# #Store country json data to file
try:

    with open("static/data/countries.json", "r") as file:
        data = json.load(file)

except Exception as e:
    print("Error reading data")


#Simplify the data
simplified_data = {country['code']: country['name'] for country in data['countries']}
db.child("data").child("countries").set(simplified_data)
print("data added to firebase database")

# Store professions json data to file
with open("static/data/professions.json", 'r') as file:
    profession_data = json.load(file)
    
db.child("data").child("profession_data").update(profession_data)
print("data updated")


profession_data = db.child("data").child("professions").get().val()

print (profession_data)