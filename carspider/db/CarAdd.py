'''
Created on 4. lip 2017.

@author: eaneivc
'''
from carspider.db.base import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

class CarAdd(Base):
	__tablename__ = 'auto_oglasi'
	__table_args__ = {'schema' : 'main'}
	
	id = Column(Integer, primary_key=True)
	link = Column(String)
	datum_objave = Column(DateTime) 
	datum = Column(DateTime)
	marka = Column(String)
	model = Column(String)
	tip = Column(String)
	cijena = Column(Integer)
	godina = Column(Integer)
	kilometri = Column(Integer)
	motor = Column(String)
	motor_snaga = Column(Integer)
	motor_obujam = Column(Integer)
	vlasnik = Column(String)
	mjenjac = Column(String)
	garaziran = Column(Boolean)
	potrosnja = Column(Integer)
	servisna_knjiga = Column(Boolean)
	prekupac = Column(Boolean)
	registracija_godina = Column(Integer)
	registracija_mjesec = Column(Integer)
	lokacija = Column(String)
	telefon = Column(String)
	web_id = Column(Integer)
	aktivan = Column(Boolean)
	novi = Column(Boolean)
	image_link = Column(String)
