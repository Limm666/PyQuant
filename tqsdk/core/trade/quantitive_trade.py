#!/usr/bin/env python
# author: limm_666
from tqsdk.ta import MACD


class quantTrade(object):
    def __init__(self, api, trade):
        self.api = api
        self.trade = trade

    def macd_trade(self, klines, quote, *args, **kwargs):
        macd = MACD(klines, 12, 26, 9)
        diff = list(macd["diff"])[-1]
        dea = list(macd["dea"])[-1]
        bar = list(macd["bar"])[-1]

        tmp_diff = list(macd["diff"])[-2]
        tmp_dea = list(macd["dea"])[-2]
        tmp_bar = list(macd["bar"])[-2]

        position = self.trade.checkPosition("DCE.y2005")
        if diff > 0 and dea > 0 and tmp_dea > tmp_diff and diff > dea:
            # 如果有仓位，先平仓，再开仓
            if position['pos'] > 0:
                order = self.trade.insertOrder("DCE.y2005", "SELL", "OPEN", position, quote.bid_price1)
            order = self.trade.insertOrder("DCE.y2005", "BUY", "OPEN", 10, quote.ask_price1)

        elif diff < 0 and dea < 0 and tmp_dea < tmp_diff and diff < dea:
            if position['pos'] < 0:
                order = self.trade.insertOrder("DCE.y2005", "SELL", "OPEN", abs(position['pos']), quote.bid_price1)
            order = self.trade.insertOrder("DCE.y2005", "SELL", "OPEN", 10, quote.bid_price1)
