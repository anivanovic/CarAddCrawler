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
        <h3 style="font-family:sans-serif, Arial;" >Pronađen novi dobar auto</h3>
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
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Marka:</span> :marka</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Model:</span> :model</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Kilometri:</span> :kilometri km</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Godina:</span> :godina. g.</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Motor:</span> :motor kW</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Garažiran:</span> :garaziran</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Prvi vlasnik:</span> :prvi</p>
                    </td>
                </tr>
                <tr style="font-family:sans-serif, Arial;" >
                    <td style="font-family:sans-serif, Arial;" >
                        <p style="font-family:sans-serif, Arial;margin-top:0;margin-bottom:0;margin-right:0;margin-left:0;" ><span class="strong" style="font-family:sans-serif, Arial;font-weight:bold;" >Registracija:</span> :registracija</p>
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

def generateMail(message):
	mail = MIMEMultipart('alternative')
	
	mail['Subject'] = 'Auto oglas ažuriranje'
	mail['From'] = 'antonije999@gmail.com'
	mail['To'] = 'antonije999@gmail.com'
	
	html = MIMEText(message, 'html')
	mail.attach(html)
	return mail.as_string()

def createAdds(res):
	adds = ''
	
	for add in res:
		addText = add_template.replace(':carImageLink', 'http://165.227.131.152/' + getStr(add.web_id) + '.jpg')
		addText = addText.replace(':marka', getStr(add.marka))
		addText = addText.replace(':model', getStr(add.model))
		addText = addText.replace(':cijena', getStr(add.cijena))
		addText = addText.replace(':kilometri', getStr(add.kilometri))
		addText = addText.replace(':godina', getStr(add.godina))
		addText = addText.replace(':motor', getStr(add.motor))
		addText = addText.replace(':garaziran', getStr(add.garaziran))
		addText = addText.replace(':prvi', getStr(add.vlasnik))
		addText = addText.replace(':registracija', getStr(add.registracija_mjesec) + '/' + getStr(add.registracija_godina))
		addText = addText.replace(':datum', getStr(add.datum_objave))
		addText = addText.replace(':carAdd', getStr(add.link))
		adds += addText
		
	return mailMessage.replace(':adds', adds)

def getCars():
	engine = connect()
	conn = engine.connect()
		
	s = select([CarAdd])\
		.where(CarAdd.cijena < 26000)\
		.where(CarAdd.godina > 2004)\
		.where(CarAdd.kilometri < 110000)\
		.where(or_(CarAdd.garaziran == True, CarAdd.garaziran == None))\
		.where(or_(CarAdd.vlasnik == 'prvi', CarAdd.vlasnik == None))\
		.where(CarAdd.aktivan == True)\
		.where(CarAdd.novi == True)\
	
	res = conn.execute(s)
	conn.close()
	if res.first():
		return res

def getAddMail():
	cars = getCars()
	if cars:
		addMessage = createAdds(cars)
		email = generateMail(addMessage)
		
		return email
	
def getStr(value):
	if value:
		return str(value)
	else:
		return ''
	
