#!/usr/bin/env python
# author: limm_666
from tqsdk.ta import MACD, tafunc
from tqsdk import TargetPosTask
from project.tools.loggerTools import logger


class quantTrade(object):
    def __init__(self, api, trade):
        self.api = api
        self.trade = trade

    def macd_trade(self, klines, quote, instrumentId, *args, **kwargs):
        macd = MACD(klines, 12, 26, 9)
        diff = list(macd["diff"])[-1]
        dea = list(macd["dea"])[-1]

        position = self.trade.checkPosition(instrumentId)
        crossup = tafunc.crossup(macd["diff"], macd["dea"])
        crossdown = tafunc.crossdown(macd["diff"], macd["dea"])
        target_pos = TargetPosTask(self.api, instrumentId)  # 创建一个自动调仓工具

        if diff > 0 and dea > 0 and list(crossup)[-1] == 1:
            # 如果有仓位，先平仓，再开仓
            if position.pos > 0:
                # 平仓
                print(" SELL close %d" % position.pos)
                target_pos.set_target_volume(0)
                # order = self.trade.insertOrder(instrumentId, "SELL", "CLOSE", position.pos, quote.bid_price1)
                if position.pos == 0:
                    print(" BUY OPEN 10")
                    order = self.trade.insertOrder(instrumentId, "BUY", "OPEN", 10, quote.ask_price1)

        elif diff < 0 and dea < 0 and list(crossdown)[-1] == 1:
            if position.pos < 0:
                # 平仓
                print(" BUY close %d" % abs(position.pos))
                target_pos.set_target_volume(0)
                # order = self.trade.insertOrder(instrumentId, "SELL", "CLOSE", position.pos, quote.bid_price1)
                if position.pos == 0:
                    print(" SELL OPEN 10")
                    order = self.trade.insertOrder(instrumentId, "SELL", "OPEN", 10, quote.bid_price1)
