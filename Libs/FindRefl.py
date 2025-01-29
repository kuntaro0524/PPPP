import os,sys,math
from argparse import ArgumentParser

class FileRefl:
    def __init__(self, root_dir):
        self.root_dir = root_dir

        # Argument analysis
        self.parser = ArgumentParser()
        self.parser.add_argument('-x', '--xdsascii', type = bool, default=False, help = 'search XDS_ASCII.HKL')
        self.parser.add_argument('-s', '--xdsascii', type = bool, default=False, help = 'search xscale.hkl')
        self.parser.add_argument('-', '--xdsascii', type = bool, default=False, help = 'search xscale.hkl')
        self.parser.add_argument('--offline', type = bool, default=False, help = 'Specify size of batch')
        args = self.parser.parse_args()
        print args

    def findXDS_ASCII_HKL(self):
        print "findXDS_ASCII_HKL"


fr = FileRefl("./")
