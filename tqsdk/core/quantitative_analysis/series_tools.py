# -*- coding:utf-8 -*- 
# author: limm_666
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import sys


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

    # 价差分析工具
    def spreadAnalysis(self, nearByCode, ForwardCode):
        nearByCodeCSV = pd.read_csv("./download/" + nearByCode + ".csv")
        ForwardCodeCSV = pd.read_csv("./download/" + ForwardCode + ".csv")

        nearByCode_close = nearByCodeCSV[nearByCode + ".close"]
        ForwardCode_close = ForwardCodeCSV[ForwardCode + ".close"]

        nearByCode_date = self.datetimeList(nearByCodeCSV["datetime"])
        ForwardCode_date = self.datetimeList(ForwardCodeCSV["datetime"])

        nearByCode_close = pd.Series(nearByCode_close.values, index=nearByCode_date)
        ForwardCode_date = pd.Series(ForwardCode_close.values, index=ForwardCode_date)
        spread = nearByCode_close - ForwardCode_date
        clear_spread = spread.dropna(axis=0, how='any')
        
        # clear_spread = pd.Series()
        # for i, v in spread.items():
        #     if not np.isnan(v):
        #         clear_spread = clear_spread.append(pd.Series([v], index=[i]))
        #

        x = clear_spread.index
        y = clear_spread.values
        avg_spread = clear_spread.sum() / clear_spread.__len__()
        plt.figure(figsize=(20, 8), dpi=80)
        plt.title('avg spread%f' % avg_spread)
        plt.plot(x, y)
        plt.show()
