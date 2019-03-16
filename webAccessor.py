import requests

class WebAccessor:    
    @staticmethod
    def get(url, query=[], timeout=0):
        while True:
            try:
                response = requests.get(url, params=query, timeout=timeout)
                if response.status_code != 200:
                    raise Exception(response.status_code)
                break
            except Exception:
                continue
            
        return response