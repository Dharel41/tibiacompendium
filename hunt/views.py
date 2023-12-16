from flask import Blueprint, jsonify, request, abort, render_template
from tibiacompendium.db import mysql
from pymysql.err import IntegrityError, DataError

# API using database cursor connection
hunt = Blueprint('hunt', __name__)

@hunt.route('/hunting-places', methods=['GET'])
def render_huntingplaces_template():
    hunt_type = request.args.get('hunt_type', 'solo')

    with mysql.cursor() as cursor:
        where_condition = "WHERE hunt_type = 'solo'" if hunt_type == 'solo' else "WHERE hunt_type = 'duo'"
        cursor.execute(
            """
            SELECT 
                COALESCE(name, ''), COALESCE(character_levels, ''), COALESCE(hunt_type, ''), COALESCE(exp_on_hour, ''), 
                COALESCE(gold_on_hour, ''), COALESCE(rune, ''), COALESCE(equipment_with_resistance, ''), COALESCE(description, '')
            FROM 
                huntingplace
            """ + where_condition)
        data = cursor.fetchall()
        return render_template('huntingplace.html', hunting_places=data, hunt_type=hunt_type)