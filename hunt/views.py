from flask import Blueprint, request, render_template, url_for, redirect, abort
from pymysql.err import IntegrityError, DataError
from tibiacompendium.db import mysql
from tibiacompendium.hunt.helpers import count_exp_speed
from tibiacompendium.hunt.validators import validate_hunting_place_data

# API using database cursor connection
hunt = Blueprint('hunt', __name__)
@hunt.route('/hunting-places', methods=['POST'])
def add_huntingplace():
    errors, validated_data = validate_hunting_place_data(request.form)

    if errors:
        return render_template('huntingplace.html', errors=errors)
    else:
        exp_on_hour = count_exp_speed(validated_data.get('exp_on_hour'), validated_data.get('exp_factor'))
        with mysql.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        INSERT INTO huntingplace 
                            (name, character_levels, hunt_type, exp_on_hour, gold_on_hour, 
                            rune, equipment_with_resistance, description)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """, 
                    (validated_data.get('name'), validated_data.get('character_levels'), validated_data.get('hunt_type'), 
                     exp_on_hour, validated_data.get('gold_on_hour'),validated_data.get('rune'), 
                     validated_data.get('eq_with_resistance'), validated_data.get('description')
                    ))
                mysql.commit()
            except (IntegrityError, DataError) as e:
                abort(400, str(e))
            
            return redirect(url_for('hunt.render_huntingplaces_template', hunt_type=validated_data.get('hunt_type')))

@hunt.route('/hunting-places', methods=['GET'])
def render_huntingplaces_template():
    hunt_type = request.args.get('hunt_type', 'solo')
    name = request.args.get('name', '')

    with mysql.cursor() as cursor:
        where_condition = "WHERE hunt_type = 'solo'" if hunt_type == 'solo' else "WHERE hunt_type = 'duo'"
        where_condition += f"AND name LIKE '%{name}%'"
        cursor.execute(
            """
            SELECT 
                COALESCE(name, ''), COALESCE(character_levels, ''), COALESCE(hunt_type, ''), COALESCE(exp_on_hour, ''), 
                COALESCE(gold_on_hour, ''), COALESCE(rune, ''), COALESCE(equipment_with_resistance, ''), COALESCE(description, '')
            FROM 
                huntingplace
            """ + where_condition + "order by exp_on_hour desc")
        data = cursor.fetchall()
        return render_template('huntingplace.html', hunting_places=data, hunt_type=hunt_type)