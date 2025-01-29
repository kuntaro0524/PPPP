#!/usr/bin/python2.6
import sys
from optparse import OptionParser


def main():
	myusage = "%prog [-tf] [-a FILE] [-n INT] arg1 arg2"
	psr = OptionParser(usage=myusage)
	psr.add_option("-a", "--add", action="store", type="string", dest="filename", default="defaulthogehoge" , metavar="FILE", help="specify an input file")
	psr.add_option("-n", type="int", dest="num" , metavar="INT", help="specify number what you want")
	psr.add_option("-t", action="store_true", dest="bool_flag", default=False , help="just flag")
	psr.add_option("-f", action="store_false", dest="bool_flag", default=0 , help="just flag")
	
	(opts, args) = psr.parse_args(sys.argv)
	print "args:\t%s" % args
	print "-a:\t%s" % opts.filename
	print "-b:\t%s" % opts.bool_flag
	# print "arg1:\t%s" % (sys.argv[1])
	# print "arg2:\t%s" % (sys.argv[2])
	print "\n\n===="
	psr.print_help()


if ( __name__ == "__main__" ):
	main()
