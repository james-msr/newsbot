import requests
from bs4 import BeautifulSoup

from ..translator import translator


class CnbcNewsParser():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    r = requests.get('https://www.cnbc.com/world/?region=world', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    news_block = None
    news = []

    def __init__(self):
        self.news_block = self.soup.find('div', id='Home Page International-riverPlus')
        self.news = self.news_block.find_all('div', class_='RiverPlusCard-cardLeft')

    def get_post_by_html(self, post):
        title_block = post.find('div', class_='RiverHeadline-headline')
        title = title_block.find_all('a')[-1]
        link = title['href']
        return {
            'title': translator.translate(title.text, dest='uz').text,
            'link': link,
        }

    # cannot get picture
    def get_post_details(self, link):
        r = requests.get(link, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

    def get_news(self):
        news_details = []
        for post in self.news:
            news_details.append(self.get_post_by_html(post))
        return news_details