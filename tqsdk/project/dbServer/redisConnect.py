# -*- coding:utf-8 -*- 
# author: limm_666

import redis

conn = redis.Redis(host='106.12.*****.***', port=6379)
conn.set('name', 'LinWOW')
print(conn.get('name'))