bind = "unix:/tmp/nginx.socket"
preload_app = True
secure_scheme_headers = {'X-FORWARDED-PROTO': 'https'}
workers = 3
worker_class = "gevent"


def pre_fork(server, worker):
    with open('/tmp/app-initialized', 'a'):
        pass
