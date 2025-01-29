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
import DirectoryProc

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

	def sendFilelist(self,filelist):
		body = 'File list'
		from_addr = 'bl32xu@gmail.com'
		to_addr = 'kunio.hirata@riken.jp'

		lines=open(filelist,"r").readlines()
		for dname in lines:
			body+="%s"%(dname)

		title="[Message from ZOO] directory list"
		body+="%5d files are existing"%len(lines)
	
		# Monitor file
		msg = self.create_message(from_addr, to_addr, title, body, 'utf-8')
		self.send_via_gmail(from_addr, to_addr, msg)

if __name__ == '__main__':

	gk=Gmail_kun()

	while(1):
		tmpfile="/isilon/users/target/target/MTPC/171208-BL32XU/tmp"
		dire="/isilon/users/target/target/MTPC/171208-BL32XU/"
		os.system("ls -latr %s/ | grep CSB > %s"%(dire,tmpfile))
		time.sleep(5)
		gk.sendFilelist(tmpfile)
		time.sleep(900)
