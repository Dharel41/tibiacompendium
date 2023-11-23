from flask import Blueprint
country = Blueprint('country', __name__)

@country.route('/')
def list():
    return 'get country' + __name__