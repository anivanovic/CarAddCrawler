'''
Created on 4. lip 2017.

@author: eaneivc
'''
from scrapy import Item, Field

class CarAddItem(Item):
	link = Field()
	datum_objave = Field() 
	datum = Field()
	cijena = Field()
	lokacija = Field()
	telefon = Field()
	aktivan = Field()
	novi = Field()
	image_link = Field()
	updated = Field()
	newsletter = Field()