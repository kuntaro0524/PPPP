import argparse

parser = argparse.ArgumentParser(description='simple example') 
parser.add_argument('bar')         
parser.add_argument('-f', '--foo') # option
parser.add_argument('-r', required=True) # required
parser.add_argument('--version', action='version', version='%(prog)s 2.0') # version
args = parser.parse_args() # implementation

print(args)

