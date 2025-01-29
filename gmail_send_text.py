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

    print body
    content = MIMEText(body, 'plain', encoding)
    alt.attach(content)

    return msg
    pass

def create_message_text(self, to_addr, subject, body, encoding):
    msg = MIMEText(body)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

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
    #to_addr = 'narita.hirotaka@gmail.com; kunio.hirata@riken.jp'
    title = "Message from ZOO"
    date="%s"%(datetime.datetime.now())
    body = "%s\n"%date

###################
    sys.path.append("/isilon/BL32XU/BLsoft/PPPP/10.Zoo/Libs")
    import Date
    import time,numpy

    time_date = Date.Date()
    loglines = open(sys.argv[1],"r").readlines()

    logline = ""
    for line in loglines:
        logline += line

    msg = create_message_text(from_addr, to_addr, title, logline, 'utf-8')
    send_via_gmail(from_addr, to_addr, msg)
