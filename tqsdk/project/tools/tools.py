# -*- coding:utf-8 -*- 
# author: limm_666
import time


def createKey(instrumentId):
    date = time.strftime("%Y-%m-%d", time.localtime())
    key = date + "::" + instrumentId
    return key
