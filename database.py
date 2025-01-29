import sqlite3
import datetime

class SQLite():

	def __init__(self):
		self.con=sqlite3.connect("BL32XU.db",isolation_level=None)

	def close(self):
		self.con.close()

	def addTable(self):
		sql=u"""
		create table beam (
			flux float,
			date text
		);"""
		self.con.execute(sql)

	def record(self,beam_flux):
		curr_time=datetime.datetime.now()
		comment="insert into beam values (%f,'%s')"%(beam_flux,curr_time)
		sql=u"%s"%comment
		self.con.execute(sql)

	def viewAll(self):
		c=self.con.cursor()
		c.execute(u"select * from beam")
		for d in c:
			print d

if __name__=="__main__":
	msq=SQLite()
	#msq.addTable()
	msq.record(1E10)
	msq.viewAll()
