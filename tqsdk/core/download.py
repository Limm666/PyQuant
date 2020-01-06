# -*- coding:utf-8 -*- 
# author: limm_666

from datetime import datetime, date
from contextlib import closing
from tqsdk import TqApi, TqSim
from tqsdk.tools import DataDownloader

api = TqApi(TqSim())
download_tasks = {}
# 下载从 2018-01-01 到 2018-09-01 的 SR901 日线数据
download_tasks["c1805"] = DataDownloader(api, symbol_list="DCE.c1805", dur_sec=24*60*60,
                    start_dt=date(2017, 9, 1), end_dt=date(2018, 9, 1), csv_file_name="DCE.c1805.csv")
download_tasks["c1809"] = DataDownloader(api, symbol_list="DCE.c1809", dur_sec=24*60*60,
                    start_dt=date(2017, 9, 1), end_dt=date(2018, 9, 1), csv_file_name="DCE.c1809.csv")
with closing(api):
    while not all([v.is_finished() for v in download_tasks.values()]):
        api.wait_update()
        print("progress: ", { k:("%.2f%%" % v.get_progress()) for k,v in download_tasks.items() })