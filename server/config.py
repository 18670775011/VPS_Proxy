# 客户端服务器配对凭证
KEYS = ['vps1', 'vps2', 'adsl']

# Flask认证配置
NEED_AUTH = True
AUTH_USER = 'admin'
AUTH_PASSWORD = '123456'

# squid代理服务器配置
SQUID_USER = 'ail'
SQUID_PW = '123456'
SQUID_PORT = 8888

# Redis数据库配置
REDIS_HOST = '127.0.0.1'
REDIS_PASSWORD = None
REDIS_PORT = 6379
TTL = 110  # 过期时间

# 验证代理IP配置
TEST_URL = 'https://www.baidu.com'
TEST_TIMEOUT = 3  # 超时时间
TEST_CYCLE = 20  # 验证间隔
