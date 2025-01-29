import sys,os,math,numpy


mydict = {"apple":1, "orange":2, "banana": 3}
print mydict.keys()
print mydict.values()
print "orange" in mydict.keys()


mydict["peach"]=4

print mydict

print "before=", mydict
# 'pop' to delete key
#mydict.pop("orange")
print "after=", mydict


dictstr = """Number of apple: %(apple)10d,
number of orange: %(orange)10d,
number of bananas: %(banana)10d""" % mydict

print dictstr
