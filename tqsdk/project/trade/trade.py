#!/usr/bin/env python
# author: limm_666

import math


class Trade(object):
    def __init__(self, api):
        self.api = api

    def insertOrder(self, instrumentId, direction, offset, volume, limit_price):
        order = self.api.insert_order(symbol=instrumentId, direction=direction, offset=offset, volume=volume,
                                      limit_price=limit_price)
        return order

    def cancelOrder(self, order):
        self.api.cancel_order(order)

    def checkPosition(self, instrumentId):
        position = self.api.get_position(instrumentId)
        return position

    def checkAcount(self):
        account = self.api.get_account()
        return account

    # 控制仓位
    def orderNum(self, quote, margin_rate):
        account = self.checkAcount()
        midPrice = (quote.bid_price1 + quote.ask_price1) / 2
        volume_multiple = quote.volume_multiple
        return math.floor(account.balance / (midPrice * volume_multiple * margin_rate * 2))
