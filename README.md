# Najua: A Quiz Webapp
#### Video Demo:  <URL HERE>
#### Description: 
Najua means I know in my native swahili. A perfect name for this quiz app that lets users create custom quizzes, play saved quizzes and keep track of quizzes taken and thier scores.

# Built With
* [![Flask][Flask.palletsprojects]][Flask-url]
* [![Bootstrap][Bootstrap.com]][Bootstrap-url]
* [![JQuery][JQuery.com]][JQuery-url]
* [![VanillaJS][VanillaJS.dev]][VanillaJS-url]
* [![Redis][Redis.io]][Redis-url]
* [![TriviaAPI][TriviaAPI.dev]][TriviaAPI-url]

## Getting Started

### Prerequisites
virtual environment
Python3


* Redis-server
```sh
sudo apt-get update  
sudo apt-get install redis-server  
sudo service redis-server start 
```
* Firebase project
go to https://console.firebase.google.com/ and configure a firebase project  
Build authentication (email & password), realtime database, and Storage  

On add firebase SDK step, copy the values for:  
```sh
apiKey:  
authDomain:  
projectId:  
storageBucket:  
messagingSenderId:  
appId:  
measurementId:  
```
Add these values to the .env file in the root folder of the app(.env.example is provided)  

Add this block to realtime database rules to enable search by username:  
```sh
{
  "rules": {
    ".read": true,
    ".write": true,
      "users": {
      ".indexOn": ["username"]
      }
  }
}
```

### Installation
Clone the repo
```sh
git clone git@github.com:bee2100cs/najua.git
```

Activate virtual environment then install flask packages:  
```sh
pip install -r requirements.txt
```

clone auth submodule  
Najua uses an auth submodule stred in a different repository that needs to be cloned into the main repo

```sh
git submodule init  
git submodule update --remote --recursive  
```
Change git remote url to avoid accidental pushes to base project
```sh
git remote set-url origin github_username/repo_name
git remote -v # confirm the changes
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Usage
Start flask app
```sh
flask run
```

Najua lets users take quizzes as anonymous users or create user accounts to keep track of quizzes taken.  
There are three types of quizzes one can take:  
1. A random Quiz:  
    User gets to set only the number of questions and they  
    are presented with a quiz with random categories, difficulty levels and quiestion type.
2. A Custom quiz:  
    Here a user has more control and they can select the category, difficulty level and answer-type(multiple or boolean)
3. Existing quiz:  
    The user takes existing quizzes created by other users.




<!-- MARKDOWN LINKS & IMAGES -->
[Flask.palletsprojects]: https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white
[Flask-url]: https://flask.palletsprojects.com/
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[Firebase.com]: https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=white
[Firebase-url]: https://firebase.google.com/
[VanillaJS.dev]: https://img.shields.io/badge/VanillaJS-FFE600?style=for-the-badge&logo=javascript&logoColor=black
[VanillaJS-url]: http://vanilla-js.com/
[Redis.io]: https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://redis.io/
[TriviaAPI.dev]: https://img.shields.io/badge/TriviaAPI-4285F4?style=for-the-badge&logo=google&logoColor=white
[TriviaAPI-url]: https://the-trivia-api.com/
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 