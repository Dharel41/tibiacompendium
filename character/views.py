import json
import urllib
from datetime import datetime
from flask import Blueprint, render_template, request

# use external API
character = Blueprint('character', __name__)

@character.route('/characters', methods=['GET'])
def render_character_template():
    character_data = []
    search_nickname = request.args.get('search')

    if search_nickname:
        nicknames = [search_nickname.replace(' ', '%20')]
    else:
        nicknames = ['Suri%20Firon', 'Dark%20Mortals', 'Lee%20Fighter']


    for nick in nicknames:
        try:
            response = urllib.request.urlopen('https://dev.tibiadata.com/v4/character/' + nick)
        except:
            return render_template('character.html', characters = [])
        else:
            data = response.read()
            json_data = json.loads(data)

            # get created dt
            if 'account_information' in json_data['character'] and 'created' in json_data['character']['account_information']:
                created = datetime.fromisoformat(json_data['character']['account_information']['created']).strftime("%d-%m-%Y %H:%M:%S")
            else:
                created = ''
            
            character_data.append({
                'name': json_data['character']['character']['name'],
                'level': json_data['character']['character']['level'],
                'vocation': json_data['character']['character']['vocation'],
                'world': json_data['character']['character']['world'],
                'residence': json_data['character']['character']['residence'],
                'achievement_points': json_data['character']['character']['achievement_points'],
                'last_login': datetime.fromisoformat(json_data['character']['character']['last_login']).strftime("%d-%m-%Y %H:%M:%S"),
                'created': created
            })

    return render_template('character.html', characters = character_data)
