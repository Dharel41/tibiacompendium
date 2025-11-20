import pymysql

# database connection
mysql = pymysql.connect( 
    host='localhost', 
    user='root',  
    password="database", 
    db='default_schema'
)

# sql alchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('mysql://root:database@localhost/default_schema')
metadata = MetaData()
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()