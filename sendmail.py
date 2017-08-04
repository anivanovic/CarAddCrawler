'''
Created on 4. kol 2017.

@author: eaneivc
'''
import smtplib
import addgen
from mail_settings import login_user, login_password, mail_addresses,\
	sender_mail


mail = addgen.getAlertCarsMail()

if mail:
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	server.login(login_user, login_password)
	
	for address in mail_addresses:
		server.sendmail(sender_mail, address, mail)
		
	server.quit()
