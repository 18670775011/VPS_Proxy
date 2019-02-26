
from flask import request, Flask, Response
import config
from functools import wraps
from db import RedisClient


def check_auth(username, password):
    if config.NEED_AUTH:
        return username == config.AUTH_USER and password == config.AUTH_PASSWORD
    else:
        return True


def authenticate():
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


app = Flask(__name__)


# 获取拨号IP，存入Redis
@app.route('/v1/pool/put/<key>', methods=['GET'])
def record(key):
    if key in config.KEYS:
        ip = request.remote_addr
        print(ip)
        redis_cli = RedisClient()
        redis_cli.put(key, ip)
        return 'Successfully saved: {}'.format(ip)
    else:
        return 'Invalid Key'


# IP代理池接口
@app.route('/v1/pool/get/', methods=['GET'])
@requires_auth  # 认证
def proxy():
    redis_cli = RedisClient()
    ip = redis_cli.random()
    if ip:
        res = ip + ':' + str(config.PORT)
        return Response(response=res, status=200)
    else:
        return Response(response='代理池为空', status=400)


# 测试页面
@app.route('/hello/', methods=['GET'])
def hello():
    return '网页正常运行！！！'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
