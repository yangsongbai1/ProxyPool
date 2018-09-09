from spider.utils import download
import time
import json


class ProxyMetaclass(type):
    ''' type(name,bases,dict)
        name -- 类的名称。
        bases -- 基类的元组。
        dict -- 字典，类内定义的命名空间变量
    '''

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFun__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFun__'].append(k)
                count += 1
        attrs['__CrawlFunCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    '''
    从各个网站爬取免费ip
    在此类下扩展添加爬虫的函数，函数名以'crawl_'开头
    '''

    def get_proxy(self, callback):
        proxies = []
        for proxy in eval('self.{}()'.format(callback)):
            proxies.append(proxy)
        return proxies

    def crawl_xici(self, max_page=15):
        '''西刺代理'''
        for page in range(max_page):
            url = 'http://www.xicidaili.com/wt/%s' % (page + 1)
            data = download(url)
            loops = data.xpath('//table[@id="ip_list"]//tr')[1:]
            for item in loops:
                ip = item.xpath('td[2]')[0].text  # ip
                port = item.xpath('td[3]')[0].text  # 端口
                protocol = item.xpath('td[6]')[0].text.lower()  # 协议
                proxy = ':'.join([ip, port])
                yield proxy

    def crawl_xiongmao(self):
        '''熊脑代理'''
        url = 'http://www.xiongmaodaili.com/xiongmao-web/freeip/list'
        data = download(url, back_response=False)
        loops = json.loads(data).get('obj')
        for item in loops:
            ip = item.get('ip')
            port = item.get('port')
            proxy = ':'.join([str(ip), str(port)])
            yield proxy

    def crawl_daili66(self, page_count=10):
        '''66代理'''
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            data = download(url)
            loops = data.xpath('''//div[@class="container"]//table//tr''')[1:]
            for item in loops:
                ip = item.xpath('td[1]')[0].text
                port = item.xpath('td[2]')[0].text
                proxy = ':'.join([ip,port])
                yield proxy


if __name__ == '__main__':
    a = Crawler()
    v= a.get_proxy('crawl_daili66')
    print(v)
