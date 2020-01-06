# -*- coding:utf-8 -*- 
# author: limm_666

def datetimeList(datetimeSeries):
    datetime_list = []
    for i, v in datetimeSeries.items():
        split = v.split(" ")
        datetime_list.append(split[0])

    return  datetime_list
