# -*- coding:utf-8 -*- 
# author: limm_666


from core.quantitative_analysis import series_tools as tools
tool = tools.AnalysisTools()


try:
    tool.spreadAnalysis("DCE.c1809", "DCE.c1805")
except FileNotFoundError as e:
    print(e)
