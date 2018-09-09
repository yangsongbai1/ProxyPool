from spider.crawler import Crawler
from spider.db import RedisOperate


class Getter:
    '''获取器，获取ip'''

    def __init__(self):
        self.crawler = Crawler()
        self.redis = RedisOperate()

    def run_getter(self):
        '''存入代理池，设置分数最高'''
        print('获取器开始运行，抓取代理中。。。')
        for callback in self.crawler.__CrawlFun__:
            # print('抓取代理的函数有',callback)
            new_proxy_list = self.crawler.get_proxy(callback)
            for proxy in new_proxy_list:
                self.redis.add(proxy)


if __name__ == '__main__':
    a = Getter()
    a.run_getter()
