# -*- coding:utf-8 -*- 
# author: limm_666

from datetime import datetime, date
from contextlib import closing
from tqsdk import TqApi, TqSim
from tqsdk.tools import DataDownloader


class DataDownload(object):
    def download(self, task, instrument_code, duration, start_time, end_time, filename):
        api = TqApi(TqSim())
        download_tasks = {}
        download_tasks[task] = DataDownloader(api, symbol_list=instrument_code, dur_sec=duration,
                                              start_dt=start_time, end_dt=end_time,
                                              csv_file_name=filename)

        # download_tasks["c1809"] = DataDownloader(api, symbol_list="DCE.c1809", dur_sec=24 * 60 * 60,
        #                                          start_dt=date(2017, 9, 1), end_dt=date(2018, 9, 1),
        #                                          csv_file_name="../DCE.c1809.csv")
        with closing(api):
            while not all([v.is_finished() for v in download_tasks.values()]):
                api.wait_update()
                print("progress: ", {k: ("%.2f%%" % v.get_progress()) for k, v in download_tasks.items()})
