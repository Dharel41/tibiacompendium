import pymysql
from flask import Flask
from tibiacompendium.city.views import city
from tibiacompendium.country.views import country

app = Flask(__name__)
app.register_blueprint(city, url_prefix='/cities')
app.register_blueprint(country, url_prefix='/countries')

# database connection feature_branch
conn = pymysql.connect( 
    host='localhost', 
    user='root',  
    password="database", 
    db='world'
)

@app.route('/')
def index():
    return 'Index Page'