#!/usr/bin/env python
# author: limm_666

import threading, time


def run(n):
    semaphpre.acquire()
    time.sleep(1)
    print("run the thread: %s \n" % n)
    semaphpre.release()


if __name__ == '__main__':
    semaphpre = threading.BoundedSemaphore(5)
    for i in range(20):
        t = threading.Thread(target=run, args=(i,))
        t.start()

while threading.active_count() != 1:
    pass
else:
    print('-----all threading.active_count()')
