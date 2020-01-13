# -*- coding:utf-8 -*- 
# author: limm_666
import sys
# sys.path.append("../")

from project.trade.trade import Trade
from project.trade.quantitive_trade import QuantTrade
from tqsdk import TqApi, TqAccount

api = TqApi(TqAccount("Z中粮期货", "****", "******"), web_gui=True)
klines = api.get_kline_serial("DCE.y2005", 10)
quote = api.get_quote("DCE.y2005")
trade = Trade(api)
account = trade.checkAcount()
while True:
    api.wait_update()
    account = trade.checkAcount()
    # if api.is_changing(klines):
    #     qt = QuantTrade(api, trade)
    #     qt.macd_trade(klines, quote, "DCE.y2005")
