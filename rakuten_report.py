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
from reportMaker import ReportMaker

# 楽天市場で市場解析する
def anlayze_market_from_rakuten(keyword):
    
    #　楽天市場から情報を取得
    rakuten = RakutenIchibaSearcher()
    products = rakuten.get_products(keyword)

    # 商品情報を解析
    market_analyzer = MarketAnalyzer()
    market_info = market_analyzer.analyze(products)

    # ランキング商品の楽天ポイントを取得
    market_info.higher_table["point"] = market_info.higher_table["link"].apply(rakuten.get_rakutenPoint)
    market_info.lower_table["point"] = market_info.lower_table["link"].apply(rakuten.get_rakutenPoint)

    # 報告レポートを作成
    pd.set_option("display.max_colwidth", 1000) # カラムの幅が省略されないようにする
    report_maker = ReportMaker(market_info)
    report_maker.make_markt_report(keyword)

def main():
    print("検索キーワードを入力してください")
    keyword = input()
    anlayze_market_from_rakuten(keyword)
    print("完了しました")

if __name__ == "__main__":
    main()