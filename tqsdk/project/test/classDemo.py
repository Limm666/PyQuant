#!/usr/bin/env python
# author: limm_666

class Demo(object):
    def __init__(self, a):
        self.a = a
        self.b = True
        self.c = True

    def run(self):
        if self.c:
            self.c = False
            self.b = True
            print("b",self.b)
            print("c",self.c)
        elif self.b:
            self.c = True
            self.b = False
            print("b",self.b)
            print("c",self.c)


demo = Demo(10)
demo.run()
demo.run()
demo.run()
demo.run()
demo.run()
