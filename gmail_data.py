#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys,os
import smtplib
import datetime
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.Utils import formatdate

def create_message(from_addr, to_addr, subject, body, encoding):
	msg = MIMEMultipart()
	msg['Subject'] = Header(subject, encoding)
	msg['From'] = from_addr
	msg['To'] = to_addr
	msg['Date'] = formatdate()

	related = MIMEMultipart('related')
	alt = MIMEMultipart('alternative')
	related.attach(alt)

	content = MIMEText(body, 'plain', encoding)
	alt.attach(content)

	#for filename in ['gonio_phi_enc.png']:
		#fp = file('%s' % filename, 'rb')
		##img = MIMEImage(fp.read(), 'png', name=filename)
		#img = MIMEImage(fp.read(), 'png', name=filename)
		#related.attach(img)
		#msg.attach(related)
	return msg
	pass

def send_via_gmail(from_addr, to_addr, msg):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('kuntaro0524@gmail.com', 'kunio335')
	s.sendmail(from_addr, [to_addr], msg.as_string())
	s.close()

if __name__ == '__main__':
	from_addr = 'kuntaro0524@gmail.com'
	to_addr = 'hirata@spring8.or.jp'
	title = "From BLPC %s/"%os.getcwd()
	date="%s"%(datetime.datetime.now())
	body = "%s\n"%date
	infile=open(sys.argv[1],'r')
	lines=infile.readlines()
	for line in lines:
		print line
		body=body+line
		
	msg = create_message(from_addr, to_addr, title, body, 'utf-8')
	send_via_gmail(from_addr, to_addr, msg)
