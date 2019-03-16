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