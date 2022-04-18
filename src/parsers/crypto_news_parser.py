from bs4 import BeautifulSoup
import requests
from ..translator import translator
import os

class CryptoNewsParser():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }

    r = requests.get('https://cryptonews.com/news/', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    news_block = None
    news = []
    lastkey = ''
    

    def __init__(self):
        self.news_block = self.soup.find('div', id='load_more_target')
        self.news = self.news_block.find_all('article', class_='mb-30')

        try:
            with open('src/keys/crypto_lastkey.txt', 'r') as f:
                self.lastkey = f.read()
        except:
            pass

    def get_post_by_html(self, post):
        title = post.find('a', class_='article__title')
        photo = post.find('img', class_='img-fluid')
        try:
            url = photo['data-src']
        except:
            url = photo['src']
        key = title['href']
        return {
            'title': translator.translate(title.text, dest='uz').text,
            'photo_url': url,
            'key': key
        }
        
    def get_news(self):
        news_details = []
        for post in self.news:
            if post.find('a', class_='article__title')['href'] != self.lastkey:
                news_details.append(self.get_post_by_html(post))
            else:
                break
        return news_details

    async def update_lastkey(self, newkey):
        with open('src/keys/crypto_lastkey.txt', 'w+') as f:
            f.write(newkey)
        self.lastkey = newkey
