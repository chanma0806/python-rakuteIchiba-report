# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import requests
from bs4 import BeautifulSoup
import markdown
import codecs
import datetime
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
import time

# 楽天市場API 
RAKUTEN_APPLICATION_ID = "1096515298420576244"
RAKUTEN_ICHIBA_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"

# コンバート用の目印
IMG_SOURCE = "img_src: "
LINK_SOURCE = "link_src: "

# 商品情報インスタンス
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

#　requests.getのラッパーメソッド
def get(url, query, timeout):
    while True:
        try:
            response = requests.get(url, params=query, timeout=timeout)
            if response.status_code != 200:
                raise Exception(response.status_code)
        except Exception as e:
            print("miss @{0}page status_code:{1}".format(query["page"], e.args[0]))
            continue
            
        return response

# xmlから商品情報にコンバートする
def convert_product_from(item):
    title = item.itemName.text if item.itemName != None else "---"
    price = int(item.itemPrice.text) if item.itemPrice != None else None
    url = item.itemUrl.text if item.itemUrl != None else "---"
    image = item.mediumImageUrls.imageUrl.text if item.mediumImageUrls.imageUrl != None else None
    return Product(title, price, url, image)
    
# レスポンスから商品情報を抽出する
def extract_products_from(soup):
    items = soup.find_all("Item")
    return list(map(lambda item: convert_product_from(item), items))

# 楽天市場から商品情報を取得する
def get_products_from_rakutenIchiba(keyword):
    
    products = []
    for page in range(1, 101):    
        # 検索クエリ
        query = {
            "format": "xml",
            "keyword" : keyword,
            "applicationId" :  RAKUTEN_APPLICATION_ID,
            "page" : page
        }
        response = get(RAKUTEN_ICHIBA_API, query=query, timeout=1)
        soup = BeautifulSoup(response.content, "xml")
        products.extend(extract_products_from(soup))
    return products

# 検索結果をテーブル化する
def convert_table(products):
    rows = list(map(lambda product: product.get_row(), products))
    return pd.DataFrame(data=rows, columns=Product.get_columns())

# htmlファイルを保存する
def save_html(date, keywords, img_price_hist, highers, lowers, links):
    source = codecs.open("test.md", mode="r", encoding="utf-8")
    text = source.read()
    html = markdown.markdown(text)
    html = html.replace("DATE", date).replace("KEYWORDS", keywords).replace("PRICE_HIST", img_price_hist).replace("HIGH_PRICE_TOP5", highers).replace("LOW_PRICE_TOP5", lowers)
    html = convert_imgTag(html)
    html = merge_link_to_title(html, links)
    html_file = codecs.open("report.html", "w", encoding="utf-8", errors="xmlcharrefreplace")
    html_file.write(html)
    html_file.close()

# イメージソースである印をつける
def mark_imgSrc(path):
    return IMG_SOURCE + path if path != None else ""
# タイトルである印をつける
def mark_titleSrc(path):
    return LINK_SOURCE + path if path != None else ""
# <table>内のイメージソースを<img>タグにコンバートする
def convert_imgTag(html):
    soup = BeautifulSoup(html, "html.parser")
    for td in soup.find_all("td", text=re.compile(IMG_SOURCE)):
        src = td.text.replace(IMG_SOURCE, "")
        imgTag = soup.new_tag("img", src=src)
        new_td = soup.new_tag("td")
        new_td.insert(0, imgTag)
        td.replace_with(new_td) 
    
    return str(soup)

# タイトルとリンクを1つのタグに束ねる
def merge_link_to_title(html, links):
    soup = BeautifulSoup(html, "html.parser")
    from IPython.core.debugger import Pdb; Pdb().set_trace()
    for td, link in zip(soup.find_all("td", text=re.compile(LINK_SOURCE)), links):
        title = td.text.replace(LINK_SOURCE, "")
        linkTag = soup.new_tag("a", href=link)
        linkTag.string = title 
        new_td = soup.new_tag("td")
        new_td.insert(0, linkTag)
        td.replace_with(new_td)

    return str(soup)

# 商品ページをスクレイピングして楽天ポイントを取得
def scraping_RakutenPoint(url):
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source.encode("utf-8"), "html.parser")
    point_summary = soup.find("div", class_ = "point-summary__total___3rYYD")
    if point_summary == None:
        return 0
    text = point_summary.find("span").text.replace(",","") # コンマ排除
    
    return int(text)

# 楽天市場レポートを作成する
def make_rakuten_report(keyword):
    # ヒストグラム画像
    SRC_PRICE_HIST = "price_hist.png"
    # ランキング
    RANK = 5
    
    #　楽天市場から情報を取得 
    products = get_products_from_rakutenIchiba(keyword)
    table = convert_table(products)

    # ヒストグラムを保存する
    table.hist(bins=100)
    plt.savefig(SRC_PRICE_HIST)

    # htmlを作成
    pd.set_option("display.max_colwidth", 1000) # カラムの幅が省略されないようにする
    table_high = table.sort_values(by=["price"], ascending=False).head(RANK)
    table_low = table.sort_values(by=["price"]).head(RANK)
    # imgタグにコンバート
    table_high["image"] = table_high["image"].apply(mark_imgSrc)
    table_low["image"] = table_low["image"].apply(mark_imgSrc)
    # タイトル情報を付与する
    table_high["title"] = table_high["title"].apply(mark_titleSrc)
    table_low["title"] = table_low["title"].apply(mark_titleSrc)
    # 楽天ポイントを算出
    table_high["point"] = table_high["link"].apply(scraping_RakutenPoint)
    table_low["point"] = table_low["link"].apply(scraping_RakutenPoint)
    # リンク情報を取り出す
    table_high_link = table_high.pop("link")
    table_low_link = table_low.pop("link")

    table_high = table_high.to_html(index=None).replace("\n", "")
    table_low = table_low.to_html(index=None).replace("\n", "")
    date = datetime.date.today().strftime("%Y-%m-%d")
    links = table_high_link.tolist()
    links.extend(table_low_link.tolist())
    save_html(date, keyword, SRC_PRICE_HIST, table_high, table_low, links)

def main():
    print("検索キーワードを入力してください")
    keyword = input()
    make_rakuten_report(keyword)
    print("完了しました")

if __name__ == "__main__":
    main()