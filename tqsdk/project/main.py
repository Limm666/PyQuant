# -*- coding:utf-8 -*- 
# author: limm_666
import sys
# sys.path.append("../")

from project.trade.trade import Trade
from project.trade.quantitive_trade import quantTrade
from tqsdk import TqApi, TqAccount

api = TqApi(TqAccount("快期模拟", "584707735@qq.com", "123456"), web_gui=True, )
klines = api.get_kline_serial("DCE.y2005", 10)
quote = api.get_quote("DCE.y2005")
trade = Trade("快期模拟", "584707735@qq.com", "123456", api)

while True:
    api.wait_update()
    if api.is_changing(klines):
        qt = quantTrade(api, trade)
        qt.macd_trade(klines, quote, "DCE.y2005")
