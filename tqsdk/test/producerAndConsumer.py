#!/usr/bin/env python
# author: limm_666

import threading
import queue

q = queue.Queue()


def producer():
    for i in range(5):
        q.put("骨头 %s" % i)
    print("开始等待所有的骨头被取走...")
    q.join()
    print("所有的骨头被取完了...")


def consumer(n):
    while q.qsize() > 0:
        print("%s 取到 " % n, q.get())
        q.task_done()  # 告知这个任务执行完了


p = threading.Thread(target=producer, )
p.start()

c1 = consumer("A")
