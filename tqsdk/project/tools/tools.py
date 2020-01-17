# -*- coding:utf-8 -*- 
# author: limm_666
import time
import threading

order_id_list = []
trade_id_list = []


def createKey(instrumentId):
    date = time.strftime("%Y-%m-%d", time.localtime())
    key = date + "::" + instrumentId
    return key


'''
新开一个线程，进行数据的存储，
1. 下场下单信息
2. 下场成交信息
'''


def RecordTradeInfo(api):
    while True:
        api.wait_update()
        order_id_list = api.get_order()
        trade_id_list = api.get_trade()
