# -*- coding:utf-8 -*- 
# author: limm_666

import socket

HOST = 'localhost'
PORT = 9000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    msg = bytes(input(">>:"), encoding="utf8")
    s.send(msg)
    data = s.recv(1024)
    print('received', data)


