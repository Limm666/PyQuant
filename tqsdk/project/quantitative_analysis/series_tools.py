# -*- coding:utf-8 -*- 
# author: limm_666
import pandas as pd
from matplotlib import pyplot as plt
from tqsdk import tafunc
import numpy as np
from tqsdk.ta import ATR

from project.download import download
from datetime import datetime, date
from pathlib import Path
import project.tools.tools as tools
from scipy import stats


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

        # 返回升序价差，密度函数，均价
        desc_series, probability_density, avg_spread = self.spreadNormalAnalysis(spread)

        plt.figure(figsize=(20, 8), dpi=80)

        plt.title('avg spread = %f' % avg_spread)
        # 数据，数组，颜色，颜色深浅，组宽，显示频率
        plt.xlabel('Spread of ' + nearByCode + '---' + ForwardCode,
                   fontdict={'family': 'Times New Roman', 'weight': 'normal', 'size': 23, })
        plt.ylabel('Frequency', fontdict={'family': 'Times New Roman', 'weight': 'normal', 'size': 23, })

        plt.hist(desc_series, bins=15, color='b', alpha=0.5, rwidth=0.6, density=True)
        plt.plot(desc_series, probability_density)

        plt.show()

        # 跨品种套利的价差分析

    def crossProuductSpread(self, productCode1, productCode2, duration, strateDate, endDate, ):
        productCode1Csv = productCode1 + ".csv"
        productCode2Csv = productCode2 + ".csv"

        productPath1 = Path("./" + productCode1Csv)
        productPath2 = Path("./" + productCode2Csv)
        try:
            if (not productPath1.is_file() and not productPath2.is_file()):
                download.download(productCode1, productCode1, duration, strateDate, endDate,
                                  "./" + productCode1 + ".csv")
                download.download(productCode2, productCode2, duration, strateDate, endDate,
                                  "./" + productCode2 + ".csv")
        except Exception as e:
            print(e)
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
        plt.plot(thetaATR.index, thetaATR.values)
        plt.plot(df["close"] / 500)
        plt.show()
        # if (thetaATR > upper):
        #     print("变化剧烈")

    # 概率密度函数
    def normfun(self, date_series, miu, sigma):
        pdf = np.exp(-((date_series - miu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
        return pdf

    # 正态分布分析
    def spreadNormalAnalysis(self, spread, confidence_intverals):
        # 升序排列
        desc_series = spread.sort_values(ascending=True)
        # 方差
        sigma = np.std(desc_series)
        # 均值
        avg_spread = np.average(desc_series)
        # 概率密度函数
        probability_density = self.normfun(desc_series, avg_spread, sigma)

        x = np.random.normal(avg_spread, sigma, 10000)
        mean, std = x.mean(), x.std(ddof=1)
        conf_intveral = stats.norm.interval(confidence_intverals, loc=avg_spread, scale=sigma)

        return desc_series, avg_spread, conf_intveral, probability_density


if __name__ == "__main__":
    tool = AnalysisTools()

    # tool.crossProuductSpread("DCE.y2009", "DCE.p2009", 60 * 60 * 24, date(2019, 11, 13), date(2020, 1, 20), )
    # tool.crossProuductSpread("KQ.i@DCE.y", "KQ.i@DCE.p", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 14), )
