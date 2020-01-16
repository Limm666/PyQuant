#!/usr/bin/env python
# author: limm_666

from multiprocessing import Process, Pipe


def f(conn):
    conn.send([42, None, 'hello'])
    print(conn.recv())
    conn.close()


if __name__ == '__main__':
    left_conn, right_conn = Pipe()
    p = Process(target=f, args=(right_conn,))
    p.start()
    print(left_conn.recv())  # prints "[42, None, 'hello']"
    left_conn.send([43, None, 'hello'])
    p.join()
