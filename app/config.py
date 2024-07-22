import os
from dotenv import load_dotenv
import redis

class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)


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

    # Sessions config
    SESSION_TYPE = "redis"
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER= True
    SESSION_REDIS = redis.from_url("redis://127.0.0.1")