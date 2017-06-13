'''
Created on 4. lip 2017.

@author: eaneivc
'''
from scrapy import Item, Field

class CarAddItem(Item):
	link = Field()
	datum_objave = Field() 
	datum = Field()
	marka = Field()
	model = Field()
	tip = Field()
	cijena = Field()
	godina = Field()
	kilometri = Field()
	motor = Field()
	motor_snaga = Field()
	motor_obujam = Field()
	vlasnik = Field()
	mjenjac = Field()
	garaziran = Field()
	potrosnja = Field()
	servisna_knjiga = Field()
	prekupac = Field()
	registracija_godina = Field()
	registracija_mjesec = Field()
	lokacija = Field()
	telefon = Field()
	web_id = Field()
	aktivan = Field()
	novi = Field()
	imageLink = Field()