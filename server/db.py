
import random
import redis
from config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, KEYS, TTL


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT):
        self.pool = redis.ConnectionPool(host=host, port=port, password=REDIS_PASSWORD)
        self.db = redis.Redis(connection_pool=self.pool)
        self.keys = KEYS
        self.ttl = TTL

    def put(self, key, proxy):
        """
        将代理IP存入Redis,访问的API的凭证key作为Redis的key值

        :param key: key值
        :param proxy: 代理IP
        :return:
        """
        self.db.set(key, proxy, ex=self.ttl)

    def random(self):
        """
        随机获取代理IP

        :return: 代理IP
        """
        key = random.choice(self.db.keys())
        proxy = self.db.get(key)

        if proxy:
            return proxy.decode()
        else:
            return None

    def all(self):
        if self.db.keys():
            return self.db.mget(self.db.keys())
        else:
            return 0


if __name__ == '__main__':
    client = RedisClient()
    # client.put('vps1', '127.0.0.1')
    # client.put('vps1', '127.0.0.3')
    client.put('vps2', '227.0.0.2')
    client.put('vps3', '45.76.212.133')
    print(client.all())
