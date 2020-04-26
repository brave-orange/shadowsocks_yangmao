#!/usr/bin/env python
# encoding=utf-8
import redis

class RedisDb:
    def __init__(self,host,port,password):
        self.pool = redis.ConnectionPool(host=host , port=port, password =password, decode_responses=True)
    def lpush(self,name,data):
        conn = redis.Redis(connection_pool=self.pool)
        conn.lpush(name,data)
    def rpush(self,name,data):
        conn = redis.Redis(connection_pool=self.pool)
        conn.rpush(name,data)
    def lrange(self,name,start,stop):
        conn = redis.Redis(connection_pool=self.pool)
        res = conn.lrange(name,start,stop)
        return res
    def lpop(self,name):
        conn = redis.Redis(connection_pool=self.pool)
        res = conn.lpop(name)
        return res
    def llen(self,name):
        conn = redis.Redis(connection_pool=self.pool)
        return conn.llen(name)
    def set(self,name,data,timeout):
        conn = redis.Redis(connection_pool=self.pool)
        return conn.set(name,data,ex=timeout)
    def get(self,name):
        conn = redis.Redis(connection_pool=self.pool)
        return conn.get(name)