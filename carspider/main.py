# coding=utf-8
import scrapy
from carspider.item import CarAddItem
from datetime import datetime
import logging

areas = [
		'dublin-2',
		'dublin-1',
		'dublin-4',
		'dublin-6',
		'grand-canal-dock'
		]

attributeMapping = {
	'Marka automobila' : 'marka',
	'Model automobila' : 'model',
	'Tip automobila' : 'tip',
	'Prva registracija' : 'godina',
	'Prijeđeni kilometri' : 'kilometri',
	'Motor' : 'motor',
	'Snaga motora' : 'motor_snaga',
	'Radni obujam' : 'motor_obujam',
	'Vlasnik' : 'vlasnik',
	'Mjenjač' : 'mjenjac',
	'Garažiran' : 'garaziran',
	'Potrošnja goriva' : 'potrosnja',
	'Servisna knjiga' : 'servisna_knjiga',
	'Registriran do' : 'registracija_godina'}


cijena = '2400'
brojSoba = '2'
minNajam = '9'
pageParam = '&page='
carParam = '&modelId='
startUrl = 'https://www.daft.ie/dublin-city/residential-property-for-rent/'

endUrl = '?ad_type=rental&advanced=1&s%5Bmxp%5D=' + cijena +\
 '&s%5Bmnb%5D=' + brojSoba + '&s%5Bmin_lease%5D=' + minNajam + '&s%5Badvanced%5D=1&s%5Bfurn%5D=1&searchSource=rental'

rootUrl = 'https://www.daft.ie'

class CarSpider(scrapy.Spider):
	name = 'carspider'
	noData = False
	
	def start_requests(self):
		for area in areas:
			self.noData = False
			for page in range(0, 5):
				offset = page * 20
				url = startUrl + area + '/' + endUrl + '&offset=' + str(offset)
				
				if not self.noData:
					yield scrapy.Request(url=url, callback=self.parse)
				else:
					continue
	
	def parse(self, response):
		if 'No results' not in response.text:
			for i, oglas in enumerate(response.css('div.search_result_title_box h2 a::attr(href)')):
				link = oglas.extract()
				followLink = rootUrl + link
				logging.info('follow link: ' + followLink)
				res = response.follow(followLink, callback=self.followCarLink)
				imageLinkList = response.css("img.main_photo::attr(src)").extract()
				imageLink = imageLinkList[i]
				logging.info('image link ' + imageLink)
				res.meta['image_link'] = imageLink
				yield res
		else:
			self.noData = True
				
				
	def followCarLink(self, response):
		selector = response.selector
		location = selector.xpath("(//div[contains(@class, 'smi-object-header')]/h1/text())[1]")
		price = selector.xpath("(//div[contains(@id, 'smi-price-string')]/text())[1]")
		logging.info(location.extract())
		logging.info(price.extract())
		

		data = {
			'link' : response.url,
			'image_link' : response.meta['image_link'],
			'datum' : datetime.now(),
			'lokacija' : location.extract_first().encode('utf-8').strip(),
			'cijena' : price.extract_first().encode('utf-8').strip(),
			'aktivan' : True,
			'novi' : True,
			'updated' : False,
			'newsletter' : True
		}
		
		return CarAddItem(data)
