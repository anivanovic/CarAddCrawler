'''
Created on 4. lip 2017.

@author: eaneivc
'''
from sqlalchemy.orm import sessionmaker
from carspider.db.db import connect
from carspider.db.CarAdd import CarAdd
from sqlalchemy.sql.expression import exists

class CarAddDbPipeline(object):
	
	def __init__(self):
		engine = connect()
		self.Session = sessionmaker(bind=engine)
		
	def process_item(self, item, spider):
		session = self.Session()
		
		carAdd = CarAdd(**item)
		
		try:
			inDb = session.query(exists().where(CarAdd.web_id == carAdd.web_id)).scalar()
			
			if not inDb:
				print('adding car to db')
				session.add(carAdd)
				session.commit()
				print('successful adding')
			else:
				print('in db. skipping car')
		except:
			session.rollback()
			raise
		finally:
			session.close()
		
		return item