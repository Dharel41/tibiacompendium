from flask import Blueprint, jsonify, request, abort, render_template
from tibiacompendium.db import mysql
from pymysql.err import IntegrityError, DataError

# simple API, using database cursor connection
city = Blueprint('city', __name__)

@city.route('/api/cities', methods=['GET'])
def get_cities():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT id, name, added_in_version, is_premium_needed as pop FROM city")
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    
@city.route('/api/cities/<string:name>', methods=['GET'])
def get_city_by_name(name):
    with mysql.cursor() as cursor:
        cursor.execute("SELECT id, name, added_in_version, is_premium_needed as pop FROM city where name = %s", name)
        data = cursor.fetchall()
        cursor.close()
        return jsonify(data)
    
@city.route('/api/cities', methods=['POST'])
def post_city():
    try:
        name = request.json['name']
    except KeyError:
        abort(400, 'Field name is required')
    else:
        is_premium_needed = request.json.get('is_premium_needed', 1)
        added_in_version = request.json.get('added_in_version', '')
    
    with mysql.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO city (name, is_premium_needed, added_in_version, added_in_version) VALUES (%s, %s)", 
                           (name, is_premium_needed, added_in_version))
            mysql.commit()
            return ({}, 204)
        except (IntegrityError, DataError) as e:
            abort(400, str(e))

@city.route('/cities', methods=['GET'])
def render_cities_template():
    with mysql.cursor() as cursor:
        cursor.execute("SELECT id, name, added_in_version, is_premium_needed as pop FROM city order by is_premium_needed, abs(added_in_version)")
        data = cursor.fetchall()
        return render_template('city.html', cities = data)