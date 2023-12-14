from flask import Flask, render_template
from tibiacompendium.city.views import city
from tibiacompendium.character.views import character

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(city)
app.register_blueprint(character)


@app.route('/')
def home():
    return render_template('home.html')