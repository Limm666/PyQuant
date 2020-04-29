# -*- coding:utf-8 -*- 
# author: limm_666

import sys
# sys.path.append("../")
from datetime import date

from tqsdk import TqApi, TqAccount, TqSim, TqReplay, TqBacktest
from project.quantitative_analysis.series_tools import AnalysisTools
from project.tools.tools import EmailService, Subject

api = TqApi(web_gui=True, account=TqSim(init_balance=100000), backtest=TqReplay(replay_dt=date(2020, 4, 2)))

y_klines = api.get_kline_serial("DCE.y2009", 60, data_length=800)
p_klines = api.get_kline_serial("DCE.p2009", 60, data_length=800)

y_quote = api.get_quote("DCE.y2009")
p_quote = api.get_quote("DCE.p2009")

tool = AnalysisTools()

subject = Subject()
subject.subject = "交易通知"
subject.sender = "自动化交易"
subject.recevier = "交易账户"

while True:
    api.wait_update()

    spread = y_klines.close - p_klines.close
    confidence_intverals = 0.8
    desc_series, avg_spread, conf_intveral, probability_density = tool.spreadNormalAnalysis(spread,
                                                                                            confidence_intverals)
    spreadPrice = y_quote.last_price - p_quote.last_price
    print("datetime", y_quote.datetime, "conf_intveral", conf_intveral, "spreadPrice=", spreadPrice)

    if spreadPrice < conf_intveral[0]:
        subject.msg = 'symbol="DCE.y2009", direction="BUY", offset="OPEN", volume=1' \
                      'symbol="DCE.p2009", direction="SELL", offset="OPEN", volume=1'
        EmailService(subject)
        print("spreadPrice::", spreadPrice, "--->   conf_intveral::", conf_intveral[0])
        api.insert_order(symbol="DCE.y2009", direction="BUY", offset="OPEN", volume=1)
        api.insert_order(symbol="DCE.p2009", direction="SELL", offset="OPEN", volume=1)
    elif spreadPrice > conf_intveral[1]:
        print("spreadPrice::", spreadPrice, "--->   conf_intveral::", conf_intveral[1])
        api.insert_order(symbol="DCE.y2009", direction="SELL", offset="OPEN", volume=1)
        api.insert_order(symbol="DCE.p2009", direction="BUY", offset="OPEN", volume=1)
