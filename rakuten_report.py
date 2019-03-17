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
import time
from rakutenIchibaSearcher import RakutenIchibaSearcher
from data import Product, MarketData
from marketAnalyzer import MarketAnalyzer

# 楽天市場API 
RAKUTEN_APPLICATION_ID = "1096515298420576244"
RAKUTEN_ICHIBA_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?"

# コンバート用の目印
IMG_SOURCE = "img_src: "
LINK_SOURCE = "link_src: "

# htmlファイルを保存する
def save_html(date, keywords, img_price_hist, highers, lowers, links):
    source = codecs.open("report_format.md", mode="r", encoding="utf-8")
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
    for td, link in zip(soup.find_all("td", text=re.compile(LINK_SOURCE)), links):
        title = td.text.replace(LINK_SOURCE, "")
        linkTag = soup.new_tag("a", href=link)
        linkTag.string = title 
        new_td = soup.new_tag("td")
        new_td.insert(0, linkTag)
        td.replace_with(new_td)

    return str(soup)

# 楽天市場レポートを作成する
def make_rakuten_report(keyword):
    # ヒストグラム画像
    SRC_PRICE_HIST = "price_hist.png"
    # ランキング
    RANK = 5
    
    #　楽天市場から情報を取得
    rakuten = RakutenIchibaSearcher()
    products = rakuten.get_products(keyword)

    # 商品情報を解析
    market_analyzer = MarketAnalyzer()
    market_info = market_analyzer.analyze(products)

    # htmlを作成
    pd.set_option("display.max_colwidth", 1000) # カラムの幅が省略されないようにする
    # imgタグにコンバート
    market_info.higher_table["image"] = market_info.higher_table["image"].apply(mark_imgSrc)
    market_info.lower_table["image"] = market_info.lower_table["image"].apply(mark_imgSrc)
    # タイトル情報を付与する
    market_info.higher_table["title"] = market_info.higher_table["title"].apply(mark_titleSrc)
    market_info.lower_table["title"] = market_info.lower_table["title"].apply(mark_titleSrc)
    # 楽天ポイントを算出
    market_info.higher_table["point"] = market_info.higher_table["link"].apply(rakuten.get_rakutenPoint)
    market_info.lower_table["point"] = market_info.lower_table["link"].apply(rakuten.get_rakutenPoint)
    # リンク情報を取り出す
    table_high_link = market_info.higher_table.pop("link")
    table_low_link = market_info.lower_table.pop("link")

    table_high = market_info.higher_table.to_html(index=None).replace("\n", "")
    table_low = market_info.lower_table.to_html(index=None).replace("\n", "")
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