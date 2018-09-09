# redis配置
REDIS_HOST = '127.0.0.1'

REDIS_PORT = 6379

REDIS_PASSWORD = ''

# redis相关键名
PROXY_POOL_ZSET = 'proxy_pool'

# 代理质量最优分数
MAX_SCORE = 10

#入库时基本分数
INITIAL_SCORE = 5

# 代理质量最差分数
MIN_SCORE = 0

# 验证周期
VERIFY_CYCLE = 20

#获取代理周期
GET_CYCLE = 60*5

# 最大批测试量
BATCH_VERIFY_SIZE = 500

# 测试url
TEST_URL = 'http://icanhazip.com/'
TEST_URLS = 'https://icanhazip.com/'

#API设置
API_HOST = '127.0.0.1'
API_PORT = 5000

#最差质量(与返回代理质量有关，不宜过低)
WORST_SCORE = 5

#API开关
API_ENABLED = True
VERIFY_ENABLED = True
GETTER_ENABLED = True
