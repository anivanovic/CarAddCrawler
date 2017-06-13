'''
Created on 4. lip 2017.

@author: eaneivc
'''
from sqlalchemy.orm import sessionmaker
from carspider.db.db import connect
from carspider.db.CarAdd import CarAdd
from sqlalchemy.sql.expression import exists
import logging
from urllib.request import urlretrieve

class CarAddDbPipeline(object):
	
	def __init__(self):
		engine = connect()
		self.newAdds = 0
		self.stillActive = 0
		self.Session = sessionmaker(bind=engine)
		
		session = self.Session()
		
		try:
			session.query(CarAdd).update({CarAdd.aktivan : False,
										CarAdd.novi : False})
			session.commit()
			logging.info('Updated car adds to active : False')
		except:
			session.rollback()
			logging.error('could not update car adds active column')
			raise
		finally:
			session.close()
			
	def close_spider(self, spider):
		logging.info('added ' + str(self.newAdds) + ' new car adds')
		logging.info(str(self.stillActive) + ' still active adds')
		
	def process_item(self, item, spider):
		session = self.Session()
		
		carAdd = CarAdd(**item)
		
		try:
			inDb = session.query(exists().where(CarAdd.web_id == carAdd.web_id)).scalar()
			
			if not inDb:
				session.add(carAdd)
				session.commit()
				urlretrieve(item.imageLink, '/usr/share/nginx/html/' + carAdd.web_id + '.jpg')
				self.newAdds += 1
			else:
				session.query(CarAdd).filter(CarAdd.web_id == carAdd.web_id).update({CarAdd.aktivan : True})
				session.commit()
				self.stillActive += 1
		except:
			session.rollback()
			logging.error('could not insert car add')
			raise
		finally:
			session.close()
		
		return item