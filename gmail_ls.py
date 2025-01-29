#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
import smtplib
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
from email.MIMEMultipart import MIMEMultipart
from email.Header import Header
from email.Utils import formatdate
import datetime

class Gmail_kun:

	def __init__(self):
		print "Gmail_kun"

	def create_message(self,from_addr, to_addr, subject, body, encoding):
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

		#filename="/isilon/BL32XU/BLsoft/PPPP/stagez.png"
		#fp = open(filename, 'rb')
		#img = MIMEImage(fp.read(), 'png', name=filename)
		#related.attach(img)
		msg.attach(related)
		return msg
		pass

	def send_via_gmail(self,from_addr, to_addr, msg):
		s = smtplib.SMTP('smtp.gmail.com', 587)
		s.ehlo()
		s.starttls()
		s.ehlo()
		s.login('bl32xu@gmail.com', 'microfocus')
		s.sendmail(from_addr, [to_addr], msg.as_string())
		s.close()

	def sendFilelist(self,currpath,monitor_file):
		body = 'File list'
		from_addr = 'bl32xu@gmail.com'
		to_addr = 'hirata@spring8.or.jp'

		path=currpath
		file_list=os.listdir(path)

		for file in file_list:
			file=os.path.join(path,file)
			stat=os.stat(file)
			last_modified = stat.st_mtime
			dt=datetime.datetime.fromtimestamp(last_modified)
			body+="%s %s\n"%(dt,file)

		title="%5d files are existing"%len(file_list)
		body+="%s is the newest one"%file
		body+="####################"
	
		# File open
		lines=open(monitor_file,"r").readlines()
		for line in lines:
			body+=line

		# Monitor file
		msg = self.create_message(from_addr, to_addr, title, body, 'utf-8')
		self.send_via_gmail(from_addr, to_addr, msg)

if __name__ == '__main__':

	gk=Gmail_kun()
	monitor_file="junk"
	while(1):
		gk.sendFilelist("./",monitor_file)
		time.sleep(900)
