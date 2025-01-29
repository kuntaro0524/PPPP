import MyException

class test1:
	def __init__(self):
		isFlag=0

	def calc(self):
		t2=test2()
		try:
			t2.scan()
		except MyException,test1_log:
			print "test1_log"
			print test1_log.args[0]

class test2:
	def __init__(self):
		isFlag=0
	def scan(self):
		print "Doing scan"
		try:
			te=3.0/0.0
		except MyException,test2_log:
			print "test2_log"
			print test2_log.args[0]
			raise MyException("%s"%test2_log)

class test3:
	def __init__(self):
		isFlag=0


if __name__=="__main__":
	t1=test1()
	try:
		t1.calc()
	except MyException,ttt:
		print ttt.args[0]
