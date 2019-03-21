# レポート作成クラス

from data import MarketData
from bs4 import BeautifulSoup
import re
import datetime
import codecs
import markdown

# コンバート用の目印
IMG_SOURCE = "img_src: "
LINK_SOURCE = "link_src: "

# レポート作成を行うクラス
class ReportMaker:
    
    def __init__(self, market_info):
        self.market_info = market_info

#-- class method--

    # レポートを作成する
    def make_markt_report(self, keyword):

        # レポート編集の下準備
        self.__mark_tag()
        table_high = self.market_info.higher_table.to_html(index=None).replace("\n", "")
        table_low = self.market_info.lower_table.to_html(index=None).replace("\n", "")
        date = datetime.date.today().strftime("%Y-%m-%d")
        table_high_link = self.market_info.higher_table.pop("link")
        table_low_link = self.market_info.lower_table.pop("link")
        links = table_high_link.tolist()
        links.extend(table_low_link.tolist())
        
        # レポート雛形を読み込み
        source = codecs.open("report_format.md", mode="r", encoding="utf-8")
        text = source.read()
        html = markdown.markdown(text)

        # htmlを編集
        html = html.replace("DATE", date).replace("KEYWORDS", keyword).replace("PRICE_HIST", self.market_info.price_hist).replace("HIGH_PRICE_TOP5", table_high).replace("LOW_PRICE_TOP5", table_low)
        html = self.__convert_imgTag(html)
        html = self.__merge_link_to_title(html, links)

        # レポートを保存
        html_file = codecs.open("report.html", "w", encoding="utf-8", errors="xmlcharrefreplace")
        html_file.write(html)
        html_file.close()


#-- private method--

    # テーブルにタグ変換用の印をつける
    def __mark_tag(self):
        # imgタグにコンバート
        self.market_info.higher_table["image"] = self.market_info.higher_table["image"].apply(self.__mark_img_src)
        self.market_info.lower_table["image"] = self.market_info.lower_table["image"].apply(self.__mark_img_src)
        # タイトル情報を付与する
        self.market_info.higher_table["title"] = self.market_info.higher_table["title"].apply(self.__mark_title)
        self.market_info.lower_table["title"] = self.market_info.lower_table["title"].apply(self.__mark_title)

    # イメージソースである印をつける
    def __mark_img_src(self, path):
        return IMG_SOURCE + path if path != None else ""

    # タイトルである印をつける
    def __mark_title(self, path):
        return LINK_SOURCE + path if path != None else ""

    # <table>内のイメージソースを<img>タグにコンバートする
    def __convert_imgTag(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for td in soup.find_all("td", text=re.compile(IMG_SOURCE)):
            src = td.text.replace(IMG_SOURCE, "")
            imgTag = soup.new_tag("img", src=src)
            new_td = soup.new_tag("td")
            new_td.insert(0, imgTag)
            td.replace_with(new_td) 
        
        return str(soup)

    # タイトルとリンクを1つのタグに束ねる
    def __merge_link_to_title(self, html, links):
        soup = BeautifulSoup(html, "html.parser")
        for td, link in zip(soup.find_all("td", text=re.compile(LINK_SOURCE)), links):
            title = td.text.replace(LINK_SOURCE, "")
            linkTag = soup.new_tag("a", href=link)
            linkTag.string = title 
            new_td = soup.new_tag("td")
            new_td.insert(0, linkTag)
            td.replace_with(new_td)

        return str(soup)