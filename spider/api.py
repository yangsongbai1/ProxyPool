import json
from flask import Flask
from spider.db import RedisOperate

app = Flask(__name__)

conn = RedisOperate()


@app.route('/')
def index():
    html = '''
        <a href='./get'>获取代理</a></br>
        <a href='./get_count'>获取代理总数</a></br>
        <a href='./get_all'>获取全部代理</a></br>
    '''
    return html


@app.route('/get')
def get():
    return conn.get_proxy()


@app.route('/get_all')
def get_all():
    all = conn.get_all()
    # a = json.dumps(all)
    return str(all)


@app.route('/get_count')
def get_count():
    return str(conn.count())


if __name__ == '__main__':
    app.debug = True
    app.run()
