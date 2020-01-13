# -*- coding:utf-8 -*- 
# author: limm_666
import sys
# sys.path.append("../")

from project.trade.trade import Trade
from project.trade.quantitive_trade import QuantTrade
from tqsdk import TqApi, TqAccount, TqSim

api = TqApi(TqSim(init_balance=10000000.0), web_gui="http://127.0.0.1:10001")
klines = api.get_kline_serial("DCE.y2005", 60)
quote = api.get_quote("DCE.y2005")
trade = Trade(api)
account = trade.checkAcount()
while True:
    api.wait_update()
    account = trade.checkAcount()
    if api.is_changing(klines):
        qt = QuantTrade(api, trade)
        qt.macd_trade(klines, quote, "DCE.y2005")
