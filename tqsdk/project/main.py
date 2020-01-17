# -*- coding:utf-8 -*- 
# author: limm_666
import sys
# sys.path.append("../")
from project.trade.trade import Trade
from project.trade.quantitive_trade import QuantTrade
from tqsdk import TqApi, TqAccount, TqSim, TqReplay
from datetime import date

# api = TqApi(backtest=TqReplay(date(2020, 1, 15)), web_gui="http://127.0.0.1:10001")
# y_klines = api.get_kline_serial("DCE.y2005", 60)
# p_klines = api.get_kline_serial("DCE.p2005", 60)
#
# y_quote = api.get_quote("DCE.y2005")
# p_quote = api.get_quote("DCE.p2005")
#
# # macdTrade = QuantTrade(api.copy(), "DCE.y2005", "macd_trade", **{"klines": y_klines, "quote": y_quote})
#
# dualThrustTrade = QuantTrade(api.copy(), "DCE.p2005", "dual_thrust_trade",
#                              **{"klines": p_klines, "NDAY": 10, "upperK1": 0.2, "downerK2": 0.2, "quote": p_quote})
#
# # macdTrade.start()
# dualThrustTrade.start()
# while True:
#     api.wait_update()
#
#     # dualThrustTrade.start()
