import scrapy
from carspider.item import CarAddItem
from datetime import datetime

carIds = [
		#"13366", #Acura
		#"10923", #Alfa Romeo
		#"10949", #Aro
		#"10952", #Aston Martin
		#"10962", #Audi
		#"10994", #Bentley
		#"11005", #BMW
		#"11030", #Cadillac
		"11041", #Chevrolet
		#"11061", #Chrysler
		"11079", #Citroen
		"11117", #Dacia
		"11119", #Daewoo
		"11134", #Daihatsu
		#"11149", #Dodge
		#"12311", #Dongfeng
		#"11160", #Ferrari
		"11179", #Fiat
		"11221", #Ford
		#"12630", #GMC
		#"11262", #Great Wall Motor
		"11268", #Honda
		#"11293", #Hummer
		"11297", #Hyundai
		#"13395", #Infiniti
		#"11321", #Isuzu
		#"11329", #Jaguar
		#"11337", #Jeep
		"11348", #Kia
		#"11372", #Lada
		#"11383", #Lamborghini
		"11389", #Lancia
		#"11408", #Land Rover
		#"11413", #Lexus
		#"11421", #Lincoln
		#"12150", #Mahindra
		#"11423", #Lotus
		#"11429", #Maserati
		#"11445", #Maybach
		"11448", #Mazda
		#"11481", #Mercedes
		#"11515", #MG
		"11517", #MINI
		"11521", #Mitsubishi
		"11540", #Nissan
		"11574", #NSU
		"11576", #Opel
		"11617", #Peugeot
		#"11657", #Pontiac
		#"11664", #Porsche
		#"12186", #Puch
		#"11679", #Proton
		"11687", #Renault
		#"11733", #Rolls-Royce
		#"11744", #Rover
		#"11774", #Saab
		#"12164", #Santana
		"11783", #Seat
		"11815", #Smart
		#"11821", #Ssang Yong
		"11827", #Subaru
		"11845", #Suzuki
		"11796", #Skoda
		#"12296", #Tata
		#"13331", #Tesla
		"11868", #Toyota
		#"11900", #Trabant
		#"12510", #UAZ
		#"11903", #USA
		"11915", #Volvo
		"11944", #VW
		#"11984", #Wartburg
		#"11988", #Yugo
		#"11997", #Zastava
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


cijena = '5000'
kilometri = '130000'
godineOd = '2003'
pageParam = '&page='
carParam = '&modelId='
startUrl = 'http://www.njuskalo.hr/rabljeni-auti?price%5Bmax%5D=' + cijena + '&yearManufactured%5Bmin%5D=' + godineOd + '&mileage%5Bmax%5D=' + kilometri
rootUrl = 'http://www.njuskalo.hr'

class CarSpider(scrapy.Spider):
	name = 'carspider'
	noData = False
	
	def start_requests(self):
		for carId in carIds:
			self.noData = False
			for page in range(1, 51):
				url = startUrl + pageParam + str(page) + carParam + carId
				
				if not self.noData:
					yield scrapy.Request(url=url, callback=self.parse)
				else:
					continue
	
	def parse(self, response):
		if 'Trenutno nema oglasa koji zadovoljavaju postavljene kriterije pretrage.' not in response.text:
			for oglas in response.css('li.EntityList-item::attr(data-href)'):
				link = oglas.extract()
				if '/auti/' in link:
					followLink = rootUrl + link
					res = response.follow(followLink, callback=self.followCarLink)
					res.meta['imgLink'] = response.xpath("//a[contains(@href, '" + link + "')]/img/@data-src").extract_first()
					yield res
		else:
			self.noData = True
				
				
	def followCarLink(self, response):
		selector = response.selector
		location = selector.xpath("(//div[contains(@class, 'passage-standard passage-standard--alpha')]//p/text())[1]")
		addId = selector.xpath("//span[contains(text(), 'Šifra oglasa:')]/../span/b/text()")
		addDate = selector.xpath("(//span[contains(text(), 'Objavljen:')]/../time/@datetime)[1]")
		phoneNumber = selector.xpath("//a[contains(@class, 'link link-tel link-tel--alpha')]/@href")
		price = selector.xpath("(//strong[contains(@class, 'price price--hrk')]/text())[1]")
		imgLink = "http:" + response.meta['imgLink']
		
		data = {
			'link' : response.url,
			'datum_objave' : datetime.strptime(addDate.extract_first()[:-6], "%Y-%m-%dT%H:%M:%S"),
			'datum' : datetime.now(),
			'prekupac' : False,
			'lokacija' : location.extract_first(),
			'cijena' : int(price.extract_first().strip().replace('.', '')),
			'web_id' : int(addId.extract_first().strip()),
			'aktivan' : True,
			'novi' : True,
			'image_link' : imgLink,
			'updated' : False,
			'newsletter' : True
		}
		
		phoneNumberStr = phoneNumber.extract_first()
		if phoneNumberStr:
			data['telefon'] = phoneNumber.extract_first().replace('tel:', ''),
		
		dataRows = selector.xpath("//table[contains(@class, 'table-summary')]//tr")
		for row in dataRows:
			name = row.xpath('th/text()').extract_first().strip().replace(':', '')
			value = row.xpath('td/text()').extract_first()
			
			if name in attributeMapping:
				self.processCarMetadata(data, name, value)
		
		return CarAddItem(data)
		
	def processCarMetadata(self, data, name, value):
		attribute = attributeMapping[name]
		
		if name == 'Registriran do':
			data['registracija_godina'] = int(value.split('/')[1])
			data['registracija_mjesec'] = int(value.split('/')[0])
		elif name == 'Prva registracija':
			data[attribute] = int(value.replace('.', ''))
		elif name == 'Snaga motora':
			data[attribute] = int(value.replace('kW', ''))
		elif name == 'Prijeđeni kilometri':
			data[attribute] = int(value.replace('km', ''))
		elif name == 'Radni obujam':
			data[attribute] = int(value.replace('cm3', ''))
		elif name == 'Potrošnja goriva':
			data[attribute] = int(round(float(value.replace(' l/100km', ''))))
		elif name == 'Servisna knjiga' or name == 'Garažiran':
			data[attribute] = value and value == 'Da'
		else:
			data[attribute] = value
		
		
		