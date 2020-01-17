# -*- coding:utf-8 -*- 
# author: limm_666

from configparser import ConfigParser
import redis
from tqsdk import TqApi, TqAccount, TqSim
import project.tools.tools as tools

cp = ConfigParser()
cp.read("./config.conf")
redis_host = cp.get("redis", "redis_host")
redis_port = cp.get("redis", "redis_port")
redis_pool = cp.get("redis", "redis_max_connections")
Pool = redis.ConnectionPool(host=redis_host, port=redis_port, max_connections=redis_pool)
conn = redis.Redis(connection_pool=Pool, decode_responses=True)

if __name__ == '__main__':
    conn.hset("hs1", "hk1", "hv1")
    print(conn.hget("hs1", "hk1"))

    dict = {
        "hk2": "hv2",
        "hk3": "hv3",
        "hk4": "hv4",
    }

    conn.hmset("hs2", dict)
    print(conn.hmget("hs2", "hk2", "hk2"))
    print(conn.hgetall("hs2"))
    print(conn.hlen("hs2"))  # 3
    print(conn.hkeys("hs2"))  #
    print(conn.hvals("hs2"))
    print(conn.hexists("hs2", "hk2"))
    print(conn.hdel("hs2", "hk2", "hk3"))
