def get_charles_proxy():
    """
    使用charles进行抓包
    """
    proxy = {'all': "http://{}:{}@{}".format('', '', '127.0.0.1:8888')}
    return proxy
