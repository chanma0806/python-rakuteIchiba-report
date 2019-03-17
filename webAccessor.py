import requests
import urllib

# webアクセス用クラス
class WebAccessor:  
    # urlにアクセスしレスポンスを返却(レスポンスが200になるまでリトライ)  
    @staticmethod
    def get(url, query=[], timeout=0):
        if WebAccessor.isAccessible(url):
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

    # urlがアクセス可能か
    @staticmethod
    def isAccessible(url):
        try:
            urllib.request.urlopen(url)
        except Exception as e:
            print(e)
            return False
        return True