# 商品情報
class Product:
    # 初期化
    def __init__(self, title, price, link, image):
        self.title = title
        self.price = price
        self.link = link
        self.image = image
        
    def get_row(self):
        return [self.title, self.price, self.link, self.image]
    
    @staticmethod
    def get_columns():
        return ["title", "price", "link", "image"]

# 市場解析データ
class MarketData:
    def __init__(self, price_hist, higher_table, lower_table):
        self.price_hist = price_hist
        self.higher_table = higher_table
        self.lower_table = lower_table