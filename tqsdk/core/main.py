# -*- coding:utf-8 -*- 
# author: limm_666


from core.quantitative_analysis import series_tools as tools
from core.download import download as dl
from datetime import datetime, date
from tqsdk import TqApi
from tqsdk.ta import MACD

api = TqApi(web_gui=True)
klines = api.get_kline_serial("DCE.y2005", 10)
quote = api.get_quote("DCE.y2005")

while True:
    api.wait_update()
    if api.is_changing(klines):
        macd = MACD(klines, 12, 26, 9)
        diff = list(macd["diff"])[-1]
        dea = list(macd["dea"])[-1]
        bar = list(macd["bar"])[-1]
        print(diff)
        print(dea)
        print(bar)
        tmp_diff = list(macd["diff"])[-2]
        tmp_dea = list(macd["dea"])[-2]
        tmp_bar = list(macd["bar"])[-2]
        print(tmp_diff)
        print(tmp_dea)
        print(tmp_bar)
        if diff > 0 and dea > 0 and tmp_dea > tmp_diff and diff > dea:
            order = api.insert_order(symbol="DCE.y2005", direction="BUY", offset="OPEN", volume=10,
                                     limit_price=quote.ask_price1)
        elif diff < 0 and dea < 0 and tmp_dea < tmp_diff and diff < dea:
            order = api.insert_order(symbol="DCE.y2005", direction="SELL", offset="OPEN", volume=10,
                                     limit_price=quote.bid_price1)
