import asyncio
import aiohttp

from spider.setting import *
from spider.db import RedisOperate


class Verifier:
    '''检测器，验证代理'''

    def __init__(self):
        self.redis = RedisOperate()
        self.test_url = TEST_URL
        self.test_urls = TEST_URLS

    async def single_verify(self, proxy):
        '''测试单个代理'''
        conn = aiohttp.TCPConnector(verify_ssl=False)  # 防止ssl报错
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get(self.test_url, proxy=real_proxy, timeout=8) as response:
                    if response.status in [200, 302]:
                        self.redis.max(proxy)
                        # print('可用，已入库')
                    else:
                        self.redis.deduction(proxy)
                        # print(response.status)
            except:
                self.redis.deduction(proxy)
                # print('不可用')

    def verify_main(self, proxy_list):
        '''主测试函数'''
        even_loop = asyncio.get_event_loop()
        tasks = [self.single_verify(proxy) for proxy in proxy_list]
        even_loop.run_until_complete(asyncio.wait(tasks))

    def run_verify(self, batch=BATCH_VERIFY_SIZE):
        '''
        运行检验器
        BATCH_VERIFY_SIZE   单批测试量
        '''
        print('检验器开始运行，正在检测代理中。。。')
        count = self.redis.count()
        print('当前有%s个代理' % count)
        for i in range(0, count, batch):
            start = i
            stop = i + batch
            proxy_list = self.redis.batch(start, stop)
            return self.verify_main(proxy_list)


if __name__ == '__main__':
    a = Verifier()
    a.run_verify()
