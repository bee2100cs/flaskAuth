import os
from dotenv import load_dotenv
import redis

load_dotenv()




class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)


    SQLALCHEMY_TRACK_MODIFICATIONS =False
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = r"sqlite:///./db.sqlite"

    # Firebase configuration
    FIREBASE_CONFIG = {
        'apiKey': os.environ.get("FIREBASE_API_KEY"),
        'authDomain': os.environ.get("FIREBASE_AUTH_DOMAIN"),
        'projectId': os.environ.get("FIREBASE_PROJECT_ID"),
        'storageBucket': os.environ.get("FIREBASE_STORAGE_BUCKET"),
        'messagingSenderId': os.environ.get("FIREBASE_MESSAGING_SENDER_ID"),
        'appId': os.environ.get("FIREBASE_APP_ID"),
        'measurementId': os.environ.get("FIREBASE_MEASUREMENT_ID"),
        'databaseURL': ""
    }

    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER= TrueSESSION_REDIS = redis.from_url("redis://127.0.0.1")
    

