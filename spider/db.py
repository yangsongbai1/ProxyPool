import redis
from random import choice
from spider.setting import *


class RedisOperate:
    '''操作redis的类'''

    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.pool = redis.ConnectionPool(host=host, port=port, password=password)
        self.db = redis.Redis(connection_pool=self.pool)
        self.proxy_pool = PROXY_POOL_ZSET

    def add(self, proxy, score=INITIAL_SCORE):
        '''
        添加到代理池
        score 代理质量分数
        INITIAL_SCORE 入库基本分数
        '''
        if not self.db.zscore(self.proxy_pool, proxy):
            return self.db.zadd(self.proxy_pool, proxy, score)


    def batch(self, start, stop):
        '''
        获取批量代理
        start 、stop     起始、结束索引
        '''
        return self.db.zrevrange(self.proxy_pool, start, stop - 1)

    def deduction(self, proxy):
        '''
        分数减1，如果小于最小值则删除
        MIN_SCORE   最小值分数
        '''
        score = self.db.zscore(self.proxy_pool, proxy)
        if score and score > MIN_SCORE:
            return self.db.zincrby(self.proxy_pool, proxy, -1)
        else:
            return self.db.zrem(self.proxy_pool,proxy)

    def max(self,proxy,score=MAX_SCORE):
        '''
        更新为最高分数
        MAX_SCORE 最高分数
        '''
        return self.db.zadd(self.proxy_pool,proxy,score)

    def count(self):
        '''return 代理数量'''
        return self.db.zcard(self.proxy_pool)

    def get_proxy(self):
        '''
        随机获取一个优质代理
        MAX_SCORE  最优质量分数
        WORST_SCORE     最差质量分数
        '''
        result = self.db.zrangebyscore(self.proxy_pool, MAX_SCORE, MAX_SCORE)
        if result:
            return choice(result)
        else:
            result = self.db.zrevrangebyscore(self.proxy_pool, MAX_SCORE, WORST_SCORE)
            if result:
                return choice(result)
            else:
                return '代理池枯竭'

    def get_all(self):
        return self.db.zrange(self.proxy_pool,0,-1)


if __name__ == '__main__':
    a = RedisOperate()
    q = a.count()
    print(q)
