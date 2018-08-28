from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL

DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'scrapy',
    'password': 'admin123',
    'database': 'stanovi'
}

def connect():
	return create_engine(URL(**DATABASE))
