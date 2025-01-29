#!/usr/bin/python
# -*- coding: utf-8 -*-
import os,sys,time
import smtplib
import datetime
import Gmail

sys.path.append("/isilon/BL32XU/BLsoft/PPPP/")

if __name__ == '__main__':
	from_addr = 'bl32xu@gmail.com'
	to_addr = 'kunio.hirata@spring8.or.jp'
	title = 'News from BL32XU'

	msg=create_message_with_logpng(from_addr, to_addr, title, 'utf-8', sys.argv[1], sys.argv[2])
	send_via_gmail(from_addr, to_addr, msg)

	send_text_file_as_email(sys.argv[1],from_addr,to_addr)
