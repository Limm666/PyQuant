#!/usr/bin/env python
# author: limm_666
from tqsdk.ta import MACD, tafunc
from tqsdk import TargetPosTask, TqApi, TqSim, TqBacktest
from project.trade.trade import Trade
from project.dbServer.redisConnect import conn
from datetime import datetime, date
from project.tools.loggerTools import logger
import project.tools.tools as tools


class QuantTrade(Trade):
    def __init__(self, api, instrumentId, strategyName, *args, **kwargs):
        super(QuantTrade, self).__init__(api)
        self.instrumentId = instrumentId
        self.strategyName = strategyName
        self.args = args
        self.kwargs = kwargs
        self.crossupflag = True
        self.crossdownflag = True

    # def macd_trade(self,klines,quote):
    def macd_trade(self):
        while True:
            self.api.wait_update()
            klines = self.kwargs['klines']
            quote = self.kwargs['quote']
            if self.api.is_changing(quote, "last_price"):
                macd = MACD(klines, 12, 26, 9)
                diff = list(macd["diff"])[-1]
                dea = list(macd["dea"])[-1]
                key = tools.createKey(self.instrumentId)
                position = self.checkPosition(self.instrumentId)
                crossup = tafunc.crossup(macd["diff"], macd["dea"])
                crossdown = tafunc.crossdown(macd["diff"], macd["dea"])
                target_pos = TargetPosTask(self.api, self.instrumentId)  # 创建一个自动调仓工具
                # 会有问题，再该分钟，和上一分钟，一直都会是下穿，或上穿状态
                # 随着行情推送，会一直有交易指示
                if list(crossup)[-1] == 1 and self.crossupflag:
                    logger.info("上穿")
                    self.crossupflag = False
                    self.crossdownflag = True
                    # 如果有仓位，先平仓，再开仓
                    if position.pos < 0:
                        # 平仓
                        print(" SELL close %d" % position.pos)
                        target_pos.set_target_volume(0)
                    if not position.pos < 0:
                        trade_volume = self.controlPosition(quote, 0.06)
                        order = self.insertOrder(self.instrumentId, "BUY", "OPEN", trade_volume, quote.ask_price1)
                        conn.lpush(key, order.__dict__)
                        logger.info(order)

                elif list(crossdown)[-1] == 1 and self.crossdownflag:
                    logger.info("下穿")
                    self.crossupflag = True
                    self.crossdownflag = False
                    if position.pos > 0:
                        # 平仓
                        logger.info(" BUY close %d" % abs(position.pos))
                        target_pos.set_target_volume(0)
                    if not position.pos > 0:
                        trade_volume = self.controlPosition(quote, 0.06)
                        self.insertOrder(self.instrumentId, "SELL", "OPEN", trade_volume, quote.bid_price1)

    # def dual_thrust_trade(self, klines, Nday, upperK1, downerK2):
    def dual_thrust_trade(self):
        while True:
            self.api.wait_update()
            klines = self.kwargs['klines']
            NDAY = self.kwargs['NDAY']  # 天数
            K1 = self.kwargs['upperK1']  # 上轨K值
            K2 = self.kwargs['downerK2']  # 下轨K值
            quote = self.kwargs['quote']  # quote

            current_open = klines.iloc[-1]["open"]
            HH = max(klines.high.iloc[-NDAY - 1:-1])  # N日最高价的最高价
            HC = max(klines.close.iloc[-NDAY - 1:-1])  # N日收盘价的最高价
            LC = min(klines.close.iloc[-NDAY - 1:-1])  # N日收盘价的最低价
            LL = min(klines.low.iloc[-NDAY - 1:-1])  # N日最低价的最低价
            range = max(HH - LC, HC - LL)
            buy_line = current_open + range * K1  # 上轨
            sell_line = current_open - range * K2  # 下轨

            if self.api.is_changing(quote, "last_price"):
                if quote.last_price > buy_line:  # 高于上轨
                    logger.info("高于上轨,目标持仓 多头3手")
                    logger.info("当前开盘价: %f, 上轨: %f, 下轨: %f" % (current_open, buy_line, sell_line))
                    logger.info()
                    target_pos.set_target_volume(3)  # 交易
                elif quote.last_price < sell_line:  # 低于下轨
                    logger.info("低于下轨,目标持仓 空头3手")
                    logger.info("当前开盘价: %f, 上轨: %f, 下轨: %f" % (current_open, buy_line, sell_line))
                    logger.info()
                    target_pos.set_target_volume(-3)  # 交易

    # def grid_trade(self):
    def grid_trade(self):
        while True:
            self.api.wait_update()
            print("grid_trade")
            print(self.kwargs["param1"])

    def run(self):
        if hasattr(self, self.strategyName):
            func = getattr(self, self.strategyName)
            return func()


if __name__ == "__main__":
    api = TqApi(TqSim(), backtest=TqBacktest(start_dt=date(2019, 8, 1), end_dt=date(2019, 10, 1)),web_gui=True )
    print("策略开始运行")

    instrumentId = "DCE.jd2005"  # 合约代码
    quote = api.get_quote(instrumentId)
    klines = api.get_kline_serial(instrumentId, 24 * 60 * 60)  # 86400使用日线
    target_pos = TargetPosTask(api, instrumentId)

    trade = QuantTrade(api,instrumentId,"macd_trade", trade=Trade(api))

    # buy_line, sell_line = trade.dual_thrust_trade(quote, klines)  # 获取上下轨

    while True:
        api.wait_update()
        # if api.is_changing(klines.iloc[-1], ["datetime", "open"]):  # 新产生一根日线或开盘价发生变化: 重新计算上下轨
        #     buy_line, sell_line = trade.dual_thrust_trade(quote, klines)
        #
        # if api.is_changing(quote, "last_price"):
        #     if quote.last_price > buy_line:  # 高于上轨
        #         print("高于上轨,目标持仓 多头3手")
        #         target_pos.set_target_volume(3)  # 交易
        #     elif quote.last_price < sell_line:  # 低于下轨
        #         print("低于下轨,目标持仓 空头3手")
        #         target_pos.set_target_volume(-3)  # 交易
        #     else:
        #         print('未穿越上下轨,不调整持仓')
    api.close()