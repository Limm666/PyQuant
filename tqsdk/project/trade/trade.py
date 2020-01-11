#!/usr/bin/env python
# author: limm_666

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
