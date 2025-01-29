import sys,os,math
from MyException import *

class ko1:
	def __init__(self):
		value=1

	def test(self):
		k2=ko2()
		try:
			k2.test2(0.0)
		raise MyException("AkanAkan")
		return -1

class ko2:
	def __init__(self):
		self.value=2

	def test2(self,bunbo):
		try:
			rtn=self.value/bunbo
		except MyException,ttt:
			print ttt.args[0]
			print "ko2,test2"
