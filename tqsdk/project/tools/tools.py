# -*- coding:utf-8 -*- 
# author: limm_666
import time
import threading


def createKey(instrumentId):
    date = time.strftime("%Y-%m-%d", time.localtime())
    key = date + "::" + instrumentId
    return key


# def RecordTradeInfo(api):
