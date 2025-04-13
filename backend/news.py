import requests
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod

class News(ABC):
    @abstractmethod
    def get_news_data():
        pass

class YahooFinanceData(News):

    def get_news_data(self):
        url = "https://finance.yahoo.com/news"

        # We can write headers to pretend the request is from a browser
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        # we can also write:
        # if not response.ok:
        if response.status_code != 200:
            print(f"Failed Requests! Status Code: {response.status_code}")
            return []

        content = response.text
        # soup is an object(a html tree), has lots of methode and function
        soup = BeautifulSoup(content, "html.parser")

        '''
        How to find elements in html file by using BeautifulSoup?
        1. soup.find(): find the first only
        2. soup.select_one(): find the first only (by CSS)
        '''

        # find <ul> container
        ul_container = soup.select_one("ul.stream-items")
        if not ul_container:
            print("ul_container not found!")
            return []

        # Select all the <li> container in <ul> container 
        li_items = ul_container.find_all("li", class_ = "stream-item")

        news_data = []
        for li in li_items:

            '''获取新闻链接'''
            a_tag = li.find("a", class_ ="subtle-link")
            # if a_tag:
            #     print('A_TAG!')
            if not a_tag:
                # print('No ATAG')
                continue

            '''获取新闻标题'''
            h3_title = li.find('h3', class_ = "clamp")
            title = h3_title.get_text(strip=True)
            link = a_tag.get("href")  # 可能是相对路径，比如 "/news/xxx.html"
            if link and link.startswith("/"):
                link = "https://finance.yahoo.com" + link

            # 9. 也许还有一个 <p> 简短描述
            p_tag = li.find("p", class_="clamp")
            summary = p_tag.get_text(strip=True) if p_tag else ""

            # 10. 存储这条新闻的数据
            news_data.append({
                "title": title,
                "link": link,
                "summary": summary
            })

        return news_data



    # news_data = fetch_news_data()
    # for idx, news in enumerate(news_data):
    #     print("--------------------------")
    #     print(f"{idx+1}.\n 标题: {news['title']}\n")
    #     print(f"链接: {news['link']}\n")
    #     print(f"概要: {news['summary']}\n")



