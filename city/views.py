from flask import Blueprint
city = Blueprint('city', __name__)

@city.route('/')
def list():
    return 'get cities' + __name__
