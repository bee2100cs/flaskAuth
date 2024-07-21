import os
from dotenv import load_dotenv


class ApplicationConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)

    