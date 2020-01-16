# -*- coding:utf-8 -*- 
# author: limm_666

import redis
from tqsdk import TqApi, TqAccount, TqSim
import project.tools.tools as tools

Pool = redis.ConnectionPool(host='106.12.193.65', port=6379, max_connections=10)
conn = redis.Redis(connection_pool=Pool, decode_responses=True)

if __name__ == '__main__':
    api = TqApi()
    quote = api.get_quote("DCE.y2005")
    while True:
        api.wait_update()
        tick_data = {
            'datetime': quote.datetime,
            'last_price': quote.last_price
        }
        key = tools.createKey("DCE.y2005")
        conn.lpush(key, tick_data)
