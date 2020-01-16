# -*- coding:utf-8 -*- 
# author: limm_666

import select
import socket
import queue

server = socket.socket()
server.bind(('localhost', 9000))
server.listen(1000)

server.setblocking(False)  # 不阻塞

msg_dic = {}
inputs = [server, ]
outputs = []
while True:
    # rlist 是让内核监测连接，如果有变化，那么返回rlist里面的链接
    # wlist 是自定义要监测是数据
    # xlist 监测异常连接i
    readable, writeable, exceptional = select.select(inputs, outputs, inputs)
    print(readable, writeable, exceptional)
    for r in readable:
        if r is server:  # 代表来了一个新连接
            conn, addr = server.accept()
            print(conn, addr)
            inputs.append(conn)  # 是因为这个新建连接还没发数据过来，就收数据所以报错
            # 所以想要实现这个客户端发数据来时，server能够知道，就需要让select监测这个conn
            # print("recived", conn.recv(1024))
            msg_dic[conn] = queue.Queue()  # 初始化一个队列，后面存要返回给客户端的队列
        else:
            data = r.recv(1024)
            print("收到数据", data)
            msg_dic[r].put(data)
            outputs.append(r)  # 放入返回的队列

    for w in writeable:
        data_to_client = msg_dic[w].get()
        w.send(data_to_client)
        outputs.remove(w)  # 确保下次的循环 不返回 已经处理完的链接

    for e in exceptional:
        if e in outputs:
            outputs.remove(e)
        inputs.remove(e)

        del msg_dic[e]
