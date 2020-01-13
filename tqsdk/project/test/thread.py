#!/usr/bin/env python
# author: limm_666

import threading
import time


def run(n):
    print("task", n)
    time.sleep(2)
    print("task done %s ::%s" % (n, threading.current_thread()))


start_time = time.time()
t_objs = []
for i in range(50):
    t = threading.Thread(target=run, args=("t-%s" % i,))
    #t.setDaemon(True) #设置守护线程,主线程执行完毕，不管子线程有没有执行完毕都退出
    t.start()
    t_objs.append(t)

# for t in t_objs:
#     t.join()
print("------all threads  has finished。。。。", threading.current_thread(), threading.active_count())
print("cost：", time.time() - start_time)

# class MyThread(threading.Thread):
#     def __init__(self, n, sleep_time):
#         super(MyThread, self).__init__()
#         self.n = n
#         self.sleep_time = sleep_time
#
#     def run(self):
#         print("running task", self.n)
#         time.sleep(self.sleep_time)
#         print("task done", self.n)
#
#
# t1 = MyThread("t1", 2)
# t2 = MyThread("t2", 4)
# t1.start()
# t2.start()
#
# t1.join()
# print("main thread")
# t2.join()
