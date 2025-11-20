from flask import Flask, render_template
from tibiacompendium.db import db_session

from tibiacompendium.city.views import city
from tibiacompendium.character.views import character
from tibiacompendium.hunt.views import hunt
from tibiacompendium.hunt.views_sql_alchemy import hunt_v2

app = Flask(__name__)
app.url_map.strict_slashes = False

# blueprints
app.register_blueprint(city)
app.register_blueprint(character)
app.register_blueprint(hunt)
app.register_blueprint(hunt_v2)


@app.route('/')
def home():
    return render_template('home.html')


# shutdown sql alchemy session
@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()