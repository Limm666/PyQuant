#!/usr/bin/env python
# author: limm_666
from logging import Logger

from tqsdk import TqApi, TqSim, TargetPosTask

from project.tools.loggerTools import logger
from project.trade import QuantTrade, Trade


def DualThrust():
    api = TqApi(TqSim(init_balance=15000.0), web_gui="http://127.0.0.1:10001")
    print("策略开始运行")

    instrumentId = "DCE.y2005"  # 合约代码
    quote = api.get_quote(instrumentId)
    klines = api.get_kline_serial(instrumentId, 24 * 60 * 60)  # 86400使用日线
    target_pos = TargetPosTask(api, instrumentId)

    trade = QuantTrade(api, Trade(api), instrumentId)

    buy_line, sell_line = trade.dual_thrust_trade(quote, klines, 5, 0.2, 0.2)  # 获取上下轨

    while True:
        api.wait_update()
        if api.is_changing(klines.iloc[-1], ["datetime", "open"]):  # 新产生一根日线或开盘价发生变化: 重新计算上下轨
            buy_line, sell_line = trade.dual_thrust_trade(quote, klines, 5, 0.2, 0.2)

        if api.is_changing(quote, "last_price"):
            if quote.last_price > buy_line:  # 高于上轨
                logger.info("高于上轨,目标持仓 多头3手")
                target_pos.set_target_volume(3)  # 交易
            elif quote.last_price < sell_line:  # 低于下轨
                logger.info("低于下轨,目标持仓 空头3手")
                target_pos.set_target_volume(-3)  # 交易
            else:
                logger.info('未穿越上下轨,不调整持仓')
DualThrust()