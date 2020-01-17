# -*- coding:utf-8 -*- 
# author: limm_666

class Trade():
    """ Trade 是一个成交对象 """

    def __init__(self, **kwargs):
        #: 委托单ID, 对于一个用户的所有委托单，这个ID都是不重复的
        self.order_id = kwargs["order_id"]
        #: 成交ID, 对于一个用户的所有成交，这个ID都是不重复的
        self.trade_id = kwargs["trade_id"]
        #: 交易所成交号
        self.exchange_trade_id = kwargs["exchange_trade_id"]
        #: 交易所
        self.exchange_id = kwargs["exchange_id"]
        #: 交易所内的合约代码
        self.instrument_id = kwargs["instrument_id"]
        #: 下单方向, BUY=买, SELL=卖
        self.direction = kwargs["direction"]
        #: 开平标志, OPEN=开仓, CLOSE=平仓, CLOSETODAY=平今
        self.offset = kwargs["offset"]
        #: 成交价格
        self.price = kwargs["price"]
        #: 成交手数
        self.volume = kwargs["volume"]
        #: 成交时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数
        self.trade_date_time = kwargs["trade_date_time"]


class Order():
    """ Order 是一个委托单对象 """

    def __init__(self, **kwargs):
        #: 委托单ID, 对于一个用户的所有委托单，这个ID都是不重复的
        self.order_id = kwargs["order_id"]
        #: 交易所单号
        self.exchange_order_id = kwargs["exchange_order_id"]
        #: 交易所
        self.exchange_id = kwargs["exchange_id"]
        #: 交易所内的合约代码
        self.instrument_id = kwargs["instrument_id"]
        #: 下单方向, BUY=买, SELL=卖
        self.direction = kwargs["direction"]
        #: 开平标志, OPEN=开仓, CLOSE=平仓, CLOSETODAY=平今
        self.offset = kwargs["offset"]
        #: 总报单手数
        self.volume_orign = kwargs["volume_orign"]
        #: 委托价格, 仅当 price_type = LIMIT 时有效
        self.limit_price = kwargs["limit_price"]
        #: 价格类型, ANY=市价, LIMIT=限价
        self.price_type = kwargs["price_type"]
        #: 下单时间，自unix epoch(1970-01-01 00:00:00 GMT)以来的纳秒数.
        self.insert_date_time = kwargs["insert_date_time"]
        #: 委托单状态信息
        self.last_msg = kwargs["last_msg"]
        #: 委托单状态, ALIVE=有效, FINISHED=已完
        self.status = kwargs["status"]
        self._this_session = False
