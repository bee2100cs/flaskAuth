from flask import Blueprint

# Create the blueprint isntance
main = Blueprint('main', __name__)

# Import the routes to register them with the blueprint
from . import routes