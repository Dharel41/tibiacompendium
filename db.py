import pymysql

# database connection
mysql = pymysql.connect( 
    host='localhost', 
    user='root',  
    password="database", 
    db='default_schema'
)