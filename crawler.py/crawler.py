import requests
from bs4 import BeautifulSoup
import pandas as pd

class NewsCrawler:
    def __init__(self, url, headers=None):
        self.url = url
        # 模拟浏览器请求头，防止被反爬
        if headers is None:
            self.headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        else:
            self.headers = headers
        self.news_list = []

    def get_html(self):
        """获取网页源码"""
        try:
            resp = requests.get(self.url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.text
        except Exception as e:
            print(f"网页请求失败：{e}")
            return None

    def parse_html(self, html):
        """解析网页，提取新闻标题、链接"""
        soup = BeautifulSoup(html, "html.parser")
        # 这里是示例选择器，实际爬取不同网站需要修改css选择器
        items = soup.select("li")
        for item in items:
            title_tag = item.select_one("a")
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href")
                if link and title:
                    self.news_list.append({"title": title, "link": link})

    def save_to_csv(self, filename="news.csv"):
        """保存数据到csv，utf-8-sig避免Excel乱码"""
        if self.news_list:
            df = pd.DataFrame(self.news_list)
            df.to_csv(filename, index=False, encoding="utf-8-sig")
            print(f"数据已保存至 {filename}，一共{len(self.news_list)}条新闻")
        else:
            print("没有抓取到新闻数据")

    def run(self):
        """爬虫主流程"""
        print("开始爬取...")
        html = self.get_html()
        if html:
            self.parse_html(html)
            self.save_to_csv()
        print("爬虫结束")

if __name__ == "__main__":
    # 测试地址，你可以换成实验指定网页
    test_url = "https://news.baidu.com/"
    crawler = NewsCrawler(test_url)
    crawler.run()
