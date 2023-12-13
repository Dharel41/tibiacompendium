from flask import Blueprint, jsonify, request, abort
from tibiacompendium.db import mysql
from pymysql.err import IntegrityError, DataError

city = Blueprint('city', __name__)

@city.route('/cities', methods=['GET'])
def get_cities():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT id, name, is_premium_needed as pop FROM city")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    
@city.route('/cities/<string:name>', methods=['GET'])
def get_city_by_name(name):
    with mysql.cursor() as cursor:
        cursor.execute("SELECT id, name, is_premium_needed as pop FROM city where name = %s", name)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    
@city.route('/cities', methods=['POST'])
def post_city():
    try:
        name = request.json['name']
    except KeyError:
        abort(400, 'Field name is required')
    else:
        is_premium_needed = request.json.get('is_premium_needed', 1)
    
    with mysql.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO city (name, is_premium_needed) VALUES (%s, %s)", (name, is_premium_needed))
            mysql.commit()
            return ({}, 204)
        except (IntegrityError, DataError) as e:
            abort(400, str(e))