import pymysql
from flask import Flask
app = Flask(__name__, instance_relative_config=True)

# database connection
conn = pymysql.connect( 
    host='localhost', 
    user='root',  
    password = "database", 
    db='world', 
    )