from flask import Flask
from tibiacompendium.city.views import city
from tibiacompendium.country.views import country

app = Flask(__name__)
app.url_map.strict_slashes = False

app.register_blueprint(city)
app.register_blueprint(country)


@app.route('/')
def index():
    return 'Index Page'