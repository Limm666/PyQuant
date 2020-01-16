# -*- coding:utf-8 -*- 
# author: limm_666
import sys
# sys.path.append("../")

import threading
from project.trade.quantitive_trade import QuantTrade
from project.DualThrust import DualThrust
from project.MACDmain import macdTrade

t1 = threading.Thread(target=macdTrade)
t2 = threading.Thread(target=DualThrust)
t1.start()
t2.start()
