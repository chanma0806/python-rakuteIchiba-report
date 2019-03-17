 
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import chromedriver_binary
from bs4 import BeautifulSoup

# スクレイピングの実行クラス
class Scraper:
    def __init__(self):
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)
    
    # コマンドに従って指定url先からスクレイピングする
    def scrape(self, url, command):
        self.driver.get(url)
        html = self.driver.page_source.encode("utf-8")
        soup = BeautifulSoup(html, "html.parser")
        element = soup.find(command.tag, attrs=command.attrs)
        scraped_value = str(element) if element != None else None

        return scraped_value

    # コマンドを作成する
    @staticmethod
    def make_command(tag, attrs, **kwargs):
        return ScraperCommand(tag, attrs)

# スクレピング用コマンド
class ScraperCommand:
    def __init__(self, tag, attrs):
            self.tag = tag
            self.attrs = attrs