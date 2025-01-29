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

def create_message(from_addr, to_addr, subject, body, encoding, pdffile):
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

	pdff = MIMEText(file(pdffile).read())
	related.attach(pdff)
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
	to_addr = 'hirata@spring8.or.jp'
	title = '[Message from ZOO]'
	body = ""

	monitor_hours=24.0
	monitor_mins=24*60.0
	monitor_step=15 # mins
	monitor_times=int(monitor_mins/monitor_step)

	zoolog="/isilon/BL32XU/BLsoft/PPPP/10.Zoo/ZooLogs/zoo_progress.log"
	pdfpath=sys.argv[1]

	body=[]
	#lines=open(zoolog,"r").readlines()
        date="%s"%(datetime.datetime.now())
        body="%s\n"%date
	#for line in lines[len(lines)-30:]:
		#body+=line
	msg = create_message(from_addr, to_addr, title, body, 'utf-8',pdfpath)
	send_via_gmail(from_addr, to_addr, msg)
	#time.sleep(monitor_step*60.0)
