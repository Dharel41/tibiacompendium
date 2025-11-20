from flask import Blueprint, Response, request, render_template, url_for, redirect, abort
from pymysql.err import IntegrityError, DataError
from tibiacompendium.db import mysql
from tibiacompendium.hunt.helpers import count_exp_speed
from tibiacompendium.hunt.validators import validate_hunting_place_data



from tibiacompendium.hunt.models import HuntingPlace
# API using SQL Alchemy
hunt_v2 = Blueprint('hunt_v2', __name__)

@hunt_v2.route('/v2/hunting-places', methods=['POST'])
def add_huntingplace():
    errors, validated_data = validate_hunting_place_data(request.form)

    if errors:
        return render_template('huntingplace_v2.html', errors=errors)
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
            
            return redirect(url_for('hunt_v2.render_huntingplaces_template', hunt_type=validated_data.get('hunt_type')))

# delete must be post method due html form restrictions
@hunt_v2.route('/v2/hunting-places/delete', methods=['POST'])    
def delete_huntingplace():
    id = request.form.get('id')

    with mysql.cursor() as cursor:
        try:
            cursor.execute(
                """
                    DELETE from huntingplace where id = %s
                """, 
                (id)
            )
        except (IntegrityError, DataError) as e:
            abort(400, str(e))
        else:
            mysql.commit()
    
    return redirect(url_for('hunt_v2.render_huntingplaces_template'))

@hunt_v2.route('/v2/hunting-places', methods=['GET'])
def render_huntingplaces_template():
    hunt_type = request.args.get('hunt_type', 'solo')
    name = request.args.get('name', '')

    data = HuntingPlace.query.filter(
            HuntingPlace.hunt_type==hunt_type
        ).order_by(
            HuntingPlace.exp_on_hour.desc()
        )
    print(data)
          

    with mysql.cursor() as cursor:
        where_condition = "WHERE hunt_type = 'solo'" if hunt_type == 'solo' else "WHERE hunt_type = 'duo'"
        where_condition += f"AND name LIKE '%{name}%'"
        cursor.execute(
            """
            SELECT 
                COALESCE(name, ''), COALESCE(character_levels, ''), COALESCE(hunt_type, ''), COALESCE(exp_on_hour, ''), 
                COALESCE(gold_on_hour, ''), COALESCE(rune, ''), COALESCE(equipment_with_resistance, ''), COALESCE(description, ''),
                id
            FROM 
                huntingplace
            """ + where_condition + "order by exp_on_hour desc")
        data = cursor.fetchall()
        return render_template('huntingplace_v2.html', hunting_places=data, hunt_type=hunt_type)