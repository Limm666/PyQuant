#!/usr/bin/env python
# author: limm_666

from multiprocessing import Process
import time


def f(name):
    time.sleep(2)
    print('hello', name)


if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
