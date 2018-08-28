# coding=utf-8
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from carspider.db.db import connect
from sqlalchemy import or_
from sqlalchemy.sql import select
from carspider.db.CarAdd import CarAdd

'''
Created on 13. lip 2017.

@author: Antonije
'''
mailMessage = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Auto oglasi</title>
</head>
<body style="font-family:sans-serif, Arial;" >
<div class="center" style="font-family:sans-serif, Arial;background-color:#eff0f1;width:600px;margin-top:auto;margin-bottom:auto;margin-right:auto;margin-left:auto;padding-bottom:20px;" >
    <div class="title" style="font-family:sans-serif, Arial;text-align:center;background-color:#5042f4;padding-top:20px;padding-bottom:20px;padding-right:20px;padding-left:20px;color:white;" >
        <h3 style="font-family:sans-serif, Arial;" >Pronaden novi stan</h3>
    </div>
    :adds
</div>
</body>
</html>
'''

add_template = '''
<div class="add" style="font-family:sans-serif, Arial;padding-top:10px;padding-bottom:10px;padding-right:10px;padding-left:10px;" >
    <div class="row" style="font-family:sans-serif, Arial;" >
        <img src=":carImageLink"
             width="200px" height="150px" alt="Slika auta" style="font-family:sans-serif, Arial;margin-top:10px;margin-bottom:10px;margin-right:10px;margin-left:10px;vertical-align:middle;border-width:0.1px;border-style:solid;border-color:black;" >
        <table style="font-family:sans-serif, Arial;display:inline-block;vertical-align:middle;" >
            <tbody style="font-family:sans-serif, Arial;" >
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Cijena:</span> :cijena kn</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Lokacija: </span> :lokacija</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Datum:</span> :datum</p>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <a href=":carAdd" style="font-family:sans-serif, Arial;color:white;text-decoration:none;" >
    <div class="link" style="font-family:sans-serif, Arial;width:150px;height:45px;border-radius:8px;background-color:#5042f4;text-align:center;vertical-align:middle;line-height:45px;margin-left:10px;" >
        Idi na oglas
    </div>
    </a>
</div>
'''

def generateMail(message, subject):
	mail = MIMEMultipart('alternative')
	
	mail['Subject'] = subject
	mail['From'] = 'antonije999@gmail.com'
	mail['To'] = 'antonije999@gmail.com'
	
	html = MIMEText(message.encode('utf-8'), 'html')
	mail.attach(html)
	return mail.as_string()

def createAdds(res):
	adds = ''
	
	for add in res:
		addText = add_template.replace(':carImageLink', getStr(add.image_link))
		addText = addText.replace(':cijena', add.cijena)
		addText = addText.replace(':datum', str(add.datum))
		addText = addText.replace(':lokacija', add.lokacija)
		addText = addText.replace(':carAdd', add.link)
		adds += addText
		
	if adds:
		return mailMessage.replace(':adds', adds)

def exeSql(sql):
	engine = connect()
	conn = engine.connect()
	
	res = conn.execute(sql)
	conn.close()
	return res
	
def getNewCars():
	sql = select([CarAdd])\
		.where(CarAdd.newsletter == True)\
		.where(CarAdd.aktivan == True)
		
	return exeSql(sql)

def getUpdatedCars():
	sql = select([CarAdd])\
		.where(CarAdd.updated == True)\
		.where(CarAdd.aktivan == True)
		
	return exeSql(sql)
	
def getCarMail(carSupplier, subject):
	cars = carSupplier()
	
	addMessage = createAdds(cars)
	
	if addMessage:
		return generateMail(addMessage, subject)

def getNewCarsMail():
	return getCarMail(getNewCars, 'Novi stanovi')

def getUpdatedCarsMail():
	return getCarMail(getUpdatedCars, 'Snižena cijena stanovima')
	
def getStr(value):
	if value:
		return str(value)
	else:
		return ''
	
