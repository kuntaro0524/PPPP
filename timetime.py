import datetime

tstr = '2012-12-29 13:49:37'
tdatetime = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S')
tdate = datetime.date(tdatetime.year, tdatetime.month, tdatetime.day)
