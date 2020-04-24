# -*- coding:utf-8 -*- 
# author: limm_666

import sys
# sys.path.append("../")

from tqsdk import TqApi, TqAccount, TqSim, TqReplay
from datetime import date
from tqsdk.ta import ATR

from project.quantitative_analysis.series_tools import AnalysisTools

api = TqApi(web_gui="http://127.0.0.1:10001")
y_klines = api.get_kline_serial("DCE.y2005", 60 * 60 * 24)
p_klines = api.get_kline_serial("DCE.p2005", 60)

y_quote = api.get_quote("DCE.y2005")
p_quote = api.get_quote("DCE.p2005")

tool = AnalysisTools()
tool.ThetaATR(y_klines, 14);
while True:
    api.wait_update()
