# -*- coding: utf-8 -*-

import pandas as pd
import os
from worker import RakutenIchibaSearcher, MarketAnalyzer, ReportMaker
from worker.appData.data import Product, MarketData

# 市場調査を実行するクラス


class Marketer:
    #-- static method--
    # 楽天市場で市場解析する
    @staticmethod
    def anlayze_market_from_rakuten(keyword):

        #　楽天市場から情報を取得
        rakuten = RakutenIchibaSearcher()
        products = rakuten.get_products(keyword)

        # 商品情報を解析
        market_analyzer = MarketAnalyzer()
        market_info = market_analyzer.analyze(products)

        # ランキング商品の楽天ポイントを取得
        market_info.higher_table["point"] = market_info.higher_table["link"].apply(
            rakuten.get_rakutenPoint)
        market_info.lower_table["point"] = market_info.lower_table["link"].apply(
            rakuten.get_rakutenPoint)

        # 報告レポートを作成
        pd.set_option("display.max_colwidth", 1000)  # カラムの幅が省略されないようにする
        report_maker = ReportMaker(market_info)
        result_path = os.path.abspath("./") + "/result/"
        report_maker.make_market_report(keyword, result_path)


def main():
    print("検索キーワードを入力してください")
    keyword = input()
    Marketer.anlayze_market_from_rakuten(keyword)
    print("完了しました")


if __name__ == "__main__":
    main()
