# -*- coding:utf-8 -*- 
# author: limm_666
import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
from tqsdk import tafunc
import numpy as np
from tqsdk.ta import ATR

from project.download import download
from datetime import datetime, date
import project.tools.tools as tools


class AnalysisTools(object):
    '''
    数据分析工具
    '''

    # 日期分析工具
    def datetimeList(self, datetimeSeries):
        datetime_list = []
        for i, v in datetimeSeries.items():
            split = v.split(" ")
            datetime_list.append(split[0])
        return datetime_list

    # 跨期价差分析工具
    def spreadAnalysis(self, nearByCode, ForwardCode):

        nearByCodeCSV = pd.read_csv("./" + nearByCode + ".csv")
        ForwardCodeCSV = pd.read_csv("./" + ForwardCode + ".csv")

        nearByCode_close = nearByCodeCSV[nearByCode + ".close"]
        ForwardCode_close = ForwardCodeCSV[ForwardCode + ".close"]

        nearByCode_date = self.datetimeList(nearByCodeCSV["datetime"])
        ForwardCode_date = self.datetimeList(ForwardCodeCSV["datetime"])

        # 创建series
        nearByCode_close = pd.Series(nearByCode_close.values, index=nearByCode_date)
        ForwardCode_close = pd.Series(ForwardCode_close.values, index=ForwardCode_date)
        spread = nearByCode_close - ForwardCode_close
        clear_spread = spread.dropna(axis=0, how='any')

        x = clear_spread.index
        y = clear_spread.values
        avg_spread = clear_spread.sum() / clear_spread.__len__()

        # 画图
        plt.figure(figsize=(20, 8), dpi=80)
        plt.title('avg spread%f' % avg_spread)
        plt.plot(x, y)
        plt.gca().xaxis.set_major_locator(ticker.MultipleLocator(10))
        plt.show()

    # 跨品种套利的价差分析
    def crossProuductSpread(self, productCode1, productCode2, duration, strateDate, endDate, ):
        download.download(productCode1, productCode1, duration, strateDate, endDate, "./" + productCode1 + ".csv")
        download.download(productCode2, productCode2, duration, strateDate, endDate, "./" + productCode2 + ".csv")
        self.spreadAnalysis(productCode1, productCode2)

    # 成交，持仓分析
    def processKline(self, kline):
        # 成交量
        trade_volume = kline["volume"]
        # 增仓量
        net_incr_volume = kline["close_oi"] - kline["open_oi"]
        # 结算价
        close = kline["close"]
        # 日期
        datetime = kline["datetime"]

        data = {
            'datetime': datetime,
            'trade_volume': trade_volume,
            'net_incr_volume': net_incr_volume,
            'close': close,
        }
        staticData = pd.DataFrame(data)
        staticData.to_csv("./download/staticData.csv")

        for index, row in staticData.iterrows():
            staticData.loc[index, 'datetime'] = tafunc.time_to_datetime(row['datetime'])

        x = staticData['datetime']
        y1 = staticData['trade_volume']
        y2 = staticData['net_incr_volume']
        y3 = staticData['close']

        # 设置图形大小
        plt.figure(figsize=(20, 8), dpi=80)
        plt.subplot(311)
        plt.ylabel("trade_volume")
        plt.plot(x, y1)

        plt.subplot(312)
        plt.ylabel("net_incr_volume")
        plt.plot(x, y2)

        plt.subplot(313)
        plt.ylabel("close")
        plt.plot(x, y3)

        plt.show()

    # 均价
    def avg_price(self, csv_name):
        csv_pd = pd.read_csv(r"../download/" + csv_name + ".csv")
        avg_price = np.average(csv_pd[csv_name + '.close'])
        print("instrument %s :%f " % (csv_name, avg_price))
        return avg_price

    # 分析成交情况
    # def analysis_trde(self, instrumentId):
    #     key = tools.createKey(instrumentId)
    #     len = redis.conn.llen(key)
    #     trade_list = []
    #     for i in range(len):
    #         trade_list.append(redis.conn.lindex(key, i))

    # ATR标准差分析
    def ThetaATR(self, df, n):
        upper = 6  # 上轨
        mid = 5  # 中轨
        lower = 4  # 下轨

        atr = ATR(df, n)
        # 标准化，每根柱子ATR 设置为5，得出比例
        ratio = atr.atr / mid
        # 算出thetaATR
        thetaATR = atr.tr / ratio
        print(thetaATR)

        plt.hlines(upper, 0, 200, colors="r")
        plt.hlines(mid, 0, 200, colors='y')
        plt.hlines(lower, 0, 200, colors='b')
        plt.plot(thetaATR.index,thetaATR.values)
        plt.plot(df["close"]/500)
        plt.show()
        # if (thetaATR > upper):
        #     print("变化剧烈")


if __name__ == "__main__":
    tool = AnalysisTools()
    tool.crossProuductSpread("DCE.y2009", "DCE.p2009", 60 * 60 * 24, date(2019, 11, 13), date(2020, 1, 20), )
    # tool.crossProuductSpread("KQ.i@DCE.y", "KQ.i@DCE.p", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 14), )
    # tool.crossProuductSpread("DCE.y2005", "DCE.p2005", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 8), )
    # c1605_avg = tool.avg_price("DCE.c1605")
    # c1705_avg = tool.avg_price("DCE.c1705")
    # c1805_avg = tool.avg_price("DCE.c1805")
    # c1905_avg = tool.avg_price("DCE.c1905")
    # c2005_avg = tool.avg_price("DCE.c2005")
    # y_avg = tool.avg_price("KQ.i@DCE.c")
    #
    # api = TqApi(TqSim())
    # klines = api.get_kline_serial("DCE.c2005", 24 * 60 * 60)
    #
    # ma60 = MA(klines, 60)
    # ma20 = MA(klines, 20)
    # ma5 = MA(klines, 5)
    #
    # # y = y_avg * 0.1 + c2005_avg * 0.2 + c1605_avg * 0.05 + c1705_avg * 0.05 + c1805_avg * 0.08 + c1905_avg * 0.08 + \
    # #     #     list(ma60["ma"])[-1] * 0.2 + list(ma20["ma"])[-1] * 0.12 + list(ma5["ma"])[-1] * 0.12
    #
    # print("ma60 :%f " % (list(ma60["ma"])[-1]))
    # print("ma20 :%f " % (list(ma20["ma"])[-1]))
    # print("ma5 :%f " % (list(ma5["ma"])[-1]))
