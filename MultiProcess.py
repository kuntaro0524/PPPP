#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import time
from multiprocessing import Process


def some_process(idx, num_process, lines):
    for line in lines[idx::num_process]:
        print "Reading %d: %s" % (idx, line.strip())
        time.sleep(1.0)  

def main():
    num_process = 4
    lines = sys.stdin.readlines()

    process_list = []
    for idx in range(num_process):
        p = Process(target=some_process, args=(idx, num_process, lines))
        process_list.append(p)
    for p in process_list:
        p.start()
    for p in process_list:
        p.join()

if __name__ == '__main__':
    main()
