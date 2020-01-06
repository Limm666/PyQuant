# -*- coding:utf-8 -*- 
# author: limm_666


from core.quantitative_analysis import series_tools as tools
from core.download import download as dl
from datetime import datetime, date
from tqsdk import TqApi

tool = tools.AnalysisTools()
dataDownload = dl.DataDownload()
api = TqApi(web_gui=True)
klines = api.get_kline_serial("DCE.y2005", 60 * 60 * 24, 50)

try:

    # 　根据k线进行分析
    tool.processKline(klines)
    #  下载数据
    # dataDownload.download("y1805", "DCE.y1805", 60 * 60 * 24, date(2017, 7, 1), date(2018, 7, 1),
    #                       "./download/DCE.y1805.csv")
    #  分析价差
    # tool.spreadAnalysis("DCE.c1809", "DCE.c1805")
except FileNotFoundError as e:
    print(e)
except Exception as e:
    print(e)

while True:
    api.wait_update()
