from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'postgres',
    'password': 'admin123',
    'database': 'auti'
}

def connect():
	return create_engine(URL(**DATABASE))
