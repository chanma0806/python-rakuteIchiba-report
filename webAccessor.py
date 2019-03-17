import requests
from urllib.parse import urlparse

# webアクセス用クラス
class WebAccessor: 

#-- static method --
    # urlにアクセスしレスポンスを返却(レスポンスが200になるまでリトライ)  
    @staticmethod
    def get(url, query={}, timeout=0):
        if not WebAccessor.is_available_scheme(url):
            raise Exception("can't access url")
        while True:
            try:
                response = requests.get(url, params=query, timeout=timeout)
                if response.status_code != 200:
                    raise Exception(response.status_code)
                break
            except Exception as e:
                continue
        return response

    #  schemeが正しいか
    @staticmethod
    def is_available_scheme(url):
        o = urlparse(url)
        return o.scheme == "http" or o.scheme == "https"