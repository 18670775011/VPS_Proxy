import threading

import requests
import time
from db import RedisClient
from config import TEST_URL, TEST_TIMEOUT, TEST_CYCLE, SQUID_PORT, SQUID_USER, SQUID_PW
from requests import RequestException


class TestProxy(threading.Thread):
    def __init__(self, proxy_list, *args, **kwargs):
        self.url = TEST_URL
        self.timeout = TEST_TIMEOUT
        self.proxy_list = proxy_list
        super().__init__(*args, **kwargs)

    def run(self):
        while self.proxy_list:
            proxy = self.proxy_list.pop().decode()
            try:
                # print('开始检查代理%s' % proxy)
                _proxy = {'https': 'https://{}:{}@{}:{}'.format(SQUID_USER, SQUID_PW, proxy, SQUID_PORT)}
                # print(_proxy)
                response = requests.get(url=self.url, proxies=_proxy, timeout=self.timeout)

                if response.status_code == 200:
                    print('%s：代理没问题' % proxy)

            except RequestException:
                print("%s：代理不可用" % proxy)
            except IndexError:
                print('代理池测试完毕！！！')


def main():
    redis_cli = RedisClient()
    while True:
        thread_list = []
        proxy_list = redis_cli.all()  # 获取所有代理

        # 多线程检测
        if proxy_list:
            for i in range(5):
                t = TestProxy(proxy_list)
                thread_list.append(t)

            for i in thread_list:
                i.start()

            for i in thread_list:
                i.join()
        else:
            print('代理池为空')

        print(f'检测完毕，暂停{TEST_CYCLE}秒')
        time.sleep(TEST_CYCLE)


if __name__ == '__main__':
    main()
