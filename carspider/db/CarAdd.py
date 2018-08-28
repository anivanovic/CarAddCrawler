'''
Created on 4. lip 2017.

@author: eaneivc
'''
from carspider.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class CarAdd(Base):
	__tablename__ = 'stanovi_oglasi'
	__table_args__ = {'schema' : 'public'}
	
	id = Column(Integer, primary_key=True)
	link = Column(String)
	datum = Column(DateTime)
	cijena = Column(String)
	lokacija = Column(String)
	image_link = Column(String)
	aktivan = Column(Boolean)
	novi = Column(Boolean)
	updated = Column(Boolean)
	newsletter = Column(Boolean)
