# -*- coding:utf-8 -*- 
# author: limm_666

from datetime import datetime, date
from contextlib import closing
from tqsdk import TqApi, TqSim
from tqsdk.tools import DataDownloader


def download(task, instrument_code, duration, start_time, end_time, filename):
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


if __name__ == "__main__":
    # download("c2005", "DCE.c2005", 60 * 60 * 24, date(2019, 6, 1), date(2020, 1, 1), "./DCE.c2005.csv")
    # download("c1905", "DCE.c1905", 60 * 60 * 24, date(2018, 6, 1), date(2019, 5, 1), "./DCE.c1905.csv")
    # download("c1805", "DCE.c1805", 60 * 60 * 24, date(2017, 6, 1), date(2018, 5, 1), "./DCE.c1805.csv")
    # download("c1705", "DCE.c1705", 60 * 60 * 24, date(2016, 6, 1), date(2017, 5, 1), "./DCE.c1705.csv")
    # download("c1605", "DCE.c1605", 60 * 60 * 24, date(2015, 6, 1), date(2018, 5, 1), "./DCE.c1605.csv")
    # download("KQ.i@DCE.c", "KQ.i@DCE.c", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 1), "./KQ.i@DCE.c.csv")
    download("KQ.i@DCE.m", "KQ.i@DCE.m", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 8), "./KQ.i@DCE.m.csv")
    download("KQ.i@DCE.y", "KQ.i@DCE.y", 60 * 60 * 24, date(2016, 6, 1), date(2020, 1, 8), "./KQ.i@DCE.y.csv")
