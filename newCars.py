'''
Created on 4. kol 2017.

@author: eaneivc
'''
import smtplib
import addgen
from carspider.db.db import connect
from sqlalchemy.orm.session import sessionmaker
from carspider.db.CarAdd import CarAdd
from mail_settings import login_user, login_password, mail_addresses,\
	sender_mail


mail = addgen.getNewCarsMail()

if mail:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(login_user, login_password)
	
	for address in mail_addresses:
		server.sendmail(sender_mail, address, mail)
	
	server.quit()
	
	engine = connect()
	conn = engine.connect()
	
	Session = sessionmaker(bind=engine)
	session = Session()
	session.query(CarAdd).update({'newsletter' : False})
	session.commit()
