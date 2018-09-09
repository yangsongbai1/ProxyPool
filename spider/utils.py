import requests
from lxml import etree

'''工具包'''


def download(url, headers=None, back_response=True,encode='utf-8', *args, **kwargs):
    '''下载url，返回xml对象'''
    if not headers:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }

    html = requests.get(url, headers=headers, **kwargs)
    html.encoding = encode
    response = etree.HTML(html.text)
    if back_response:
        return response
    else:
        return html.text
