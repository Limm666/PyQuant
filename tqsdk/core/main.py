# -*- coding:utf-8 -*- 
# author: limm_666

import sys
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from core import series_tools

c1905 = pd.read_csv("./DCE.c1805.csv")
c1909 = pd.read_csv("./DCE.c1809.csv")

c1909_close = c1909["DCE.c1809.close"]
c1905_close = c1905["DCE.c1805.close"]
print(type(c1905.columns))
print(type(c1909.values))
print(c1909.index)
c1909_date = series_tools.datetimeList(c1909["datetime"])
c1905_date = series_tools.datetimeList(c1905["datetime"])

c1909_close = pd.Series(c1909_close.values, index=c1909_date)
c1905_close = pd.Series(c1905_close.values, index=c1905_date)
spread = c1909_close - c1905_close
clear_spread = pd.Series()
# tmp = spread.dropna(axis=0, how='any')
for i, v in spread.items():
    if not np.isnan(v):
        clear_spread = clear_spread.append(pd.Series([v], index=[i]))

x = clear_spread.index
y = clear_spread.values

plt.figure(figsize=(20, 8), dpi=80)
plt.title('avg spread%f'%(clear_spread.sum()/clear_spread.__len__()))
plt.plot(x,y)
plt.show()
print(clear_spread)
