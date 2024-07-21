import os
from dotenv import load_dotenv
import redis

load_dotenv()




class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)


    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'auth.db')

    # Firebase configuration
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get("apiKey"),
        'authDomain': os.environ.get("authDomain"),
        'projectId': os.environ.get("projectId"),
        'storageBucket': os.environ.get("storageBucket"),
        'messagingSenderId': os.environ.get("messagingSenderId"),
        'appId': os.environ.get("appId"),
        'measurementId': os.environ.get("measurementId"),
        'databaseURL': os.environ.get("database_url")
    }

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER= TrueSESSION_REDIS = redis.from_url("redis://127.0.0.1")
    

