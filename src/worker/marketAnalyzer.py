from .appData.data import Product, MarketData
from matplotlib import pyplot as plt
import pandas as pd

# ランキングの表示数
RANK = 5
# ヒストグラムの保存先
SRC_PRICE_HIST = "price_hist.png"


class MarketAnalyzer:

    #-- class method --
    # 商品情報から市場解析結果を出力する
    def analyze(self, products):

        if products == None or len(products) < 1:
            return None
        table = self.__convert_table(products)
        price_hist = table["price"].hist(bins=100)
        higher = table.sort_values(by=["price"], ascending=False).head(RANK)
        lower = table.sort_values(by=["price"]).head(RANK)

        return MarketData(price_hist, higher, lower)

#-- private method --
    # 商品情報をテーブル化する
    def __convert_table(self, products):
        rows = list(map(lambda product: product.get_row(), products))
        return pd.DataFrame(data=rows, columns=Product.get_columns())
