from webAccessor import WebAccessor
from bs4 import BeautifulSoup
from data import Product
import pandas as pd

RAKUTEN_APPLICATION_ID = "1096515298420576244"
RAKUTEN_ICHIBA_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"

class RakutenIchibaSearcher:

#-- class method -- 
    # 楽天市場から商品情報を取得する
    def get_products(self, keyword):
        products = []
        for page in range(1, 101):    
            # 検索クエリ
            query = {
                "format": "xml",
                "keyword" : keyword,
                "applicationId" :  RAKUTEN_APPLICATION_ID,
                "page" : page
            }
            response = WebAccessor.get(RAKUTEN_ICHIBA_API, query=query, timeout=1)
            soup = BeautifulSoup(response.content, "xml")
            products.extend(self.__extract_products_from(soup))
        
        return products

#-- private method --

    # レスポンスから商品情報を抽出する
    def __extract_products_from(self, soup):
        items = soup.find_all("Item")
        return list(map(lambda item: self.__convert_product_from(item), items))

    # xmlから商品情報にコンバートする
    def __convert_product_from(self, item):
        title = item.itemName.text if item.itemName != None else "---"
        price = int(item.itemPrice.text) if item.itemPrice != None else None
        url = item.itemUrl.text if item.itemUrl != None else "---"
        image = item.mediumImageUrls.imageUrl.text if item.mediumImageUrls.imageUrl != None else None
        return Product(title, price, url, image)