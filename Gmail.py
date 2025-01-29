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

class Gmail:
	def __init__(self):
		self.from_addr = 'bl32xu@gmail.com'
		self.title = 'News from BL32XU'

	def create_message_with_logpng(to_addr, subject, encoding, logfile, pngfile):
		msg = MIMEMultipart()
		msg['Subject'] = Header(subject, encoding)
		msg['From'] = self.from_addr
		msg['To'] = to_addr
		msg['Date'] = formatdate()
	
		body=""
		## LOGFILE
        	lines=open(logfile,"r").readlines()
        	for line in lines:
                	body=body+line
	
		related = MIMEMultipart('related')
		alt = MIMEMultipart('alternative')
		related.attach(alt)
	
		content = MIMEText(body, 'plain', encoding)
		alt.attach(content)
	
		fp = open(pngfile, 'rb')
		nm=pngfile.replace(".","").replace("/","")
		img = MIMEImage(fp.read(), 'png', name=pngfile)
		related.attach(img)
		msg.attach(related)
		return msg
	
	def create_message(to_addr, subject, body, encoding):
		msg = MIMEMultipart()
		msg['Subject'] = Header(subject, encoding)
		msg['From'] = self.from_addr
		msg['To'] = to_addr
		msg['Date'] = formatdate()
	
		related = MIMEMultipart('related')
		alt = MIMEMultipart('alternative')
		related.attach(alt)
	
		content = MIMEText(body, 'plain', encoding)
		alt.attach(content)
	
		filename="/isilon/BL32XU/BLsoft/PPPP/stagez.png"
		fp = open(filename, 'rb')
		img = MIMEImage(fp.read(), 'png', name=filename)
		related.attach(img)
		msg.attach(related)
		return msg
		pass
	
	def create_message_text(self, to_addr, subject, body, encoding):
		msg = MIMEText(body)
		msg['Subject'] = Header(subject, encoding)
		msg['From'] = self.from_addr
		msg['To'] = to_addr
		msg['Date'] = formatdate()
	
		return msg
		pass
	
	def send_text_file_as_email(self,to_addr,filename,title):
        	date="%s"%(datetime.datetime.now())
		body="#######################\n"
        	body+="%s\n"%date
		body+="#######################\n"
        	lines=open(filename,"r").readlines()
        	for line in lines:
                	body=body+line
		msg = self.create_message_text(to_addr, title, body, 'utf-8')
		self.send_via_gmail(to_addr, msg)
	
	def send_via_gmail(self, to_addr, msg):
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login('bl32xu@gmail.com', 'microfocus')
		s.sendmail(self.from_addr, [to_addr], msg.as_string())
		s.close()
	
if __name__ == '__main__':
	#msg=create_message_with_logpng(self.from_addr, to_addr, title, 'utf-8', sys.argv[1], sys.argv[2])
	#send_via_gmail(self.from_addr, to_addr, msg)

	gmail=Gmail()
	gmail.send_text_file_as_email(sys.argv[1],sys.argv[2],sys.argv[3])
