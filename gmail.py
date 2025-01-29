#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
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

	filename="/isilon/BL32XU/BLsoft/Logs/Zoo/025_dtheta1.png"
	fp = open(filename, 'rb')
	img = MIMEImage(fp.read(), 'png', name=filename)
	related.attach(img)
	msg.attach(related)
	return msg
	pass

def send_via_gmail(from_addr, to_addr, msg):
	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.ehlo()
	s.starttls()
	s.ehlo()
	s.login('bl32xu@gmail.com', 'microfocus')
	s.sendmail(from_addr, [to_addr], msg.as_string())
	s.close()

if __name__ == '__main__':
	from_addr = 'bl32xu@gmail.com'
	to_addr = 'kunio.hirata@riken.jp'
	title = 'Message from ZOO'
	body = ""

        date="%s"%(datetime.datetime.now())
        body = "%s\n"%date
        infile=open(sys.argv[1],'r')
        lines=infile.readlines()

        for line in lines:
                body=body+line

	msg = create_message(from_addr, to_addr, title, body, 'utf-8')
	send_via_gmail(from_addr, to_addr, msg)
