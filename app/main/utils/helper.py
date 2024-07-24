import hashlib
import requests


# Generate session token from Trivia API
#  to keep track of questions the API has already retrieved.
def fetch_session_token():
    global session_token
    response_code = None
    response = requests.get('https://opentdb.com/api_token.php?command=request')
    data = response.json()
    session_token = data.get('token')
    return session_token

# Function to fetch data from Trivia API
def fetch_data_from_api(api_url):
    global session_token
    response = requests.get(f'{api_url}&token={session_token}')
    response.raise_for_status()
    data = response.json()
    if data.get('response_code') in (4, 3):
        # Generate new token
        session_token = fetch_session_token()
        response = requests.get(f'{api_url}&token={session_token}')
    return data

# Function to get category Id from DB
def get_key_by_value(data_dict, target_value):
    for key, value in data_dict.items():
        if key == target_value:
            return value
    return None


# Function to Generate a unique ID based on the string of the question 
# using hashing function
# so that the same question will always generate the same unique ID
# ensuring that no duplicate questions are added to the database
def generate_question_id(question_text):
    return hashlib.sha256(question_text.encode('utf-8')).hexdigest()



