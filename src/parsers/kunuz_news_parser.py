from bs4 import BeautifulSoup
import requests


class KunuzNewsParser():
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

    r = requests.get('https://kun.uz/news/list', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    news_block = None
    news = []
    lastkey = ''

    def __init__(self):
        self.news_block = self.soup.find('div', class_='daily-news')
        self.news = self.news_block.find_all('a', class_='daily-block')

        try:
            with open('src/keys/kunuz_lastkey.txt', 'r') as f:
                self.lastkey = f.read()
        except:
            pass

    def get_post_by_html(self, post):
        title = post.find('p', class_='news-title')
        key = post['href']
        more = 'https://kun.uz' + key
        return {
            'title': title.text,
            'key': key,
            'more': more
        }

    def get_news(self):
        news_details = []
        for post in self.news:
            if post['href'] != self.lastkey:
                news_details.append(self.get_post_by_html(post))
            else:
                break
        return news_details

    async def update_lastkey(self, newkey):
        with open('src/keys/kunuz_lastkey.txt', 'w+') as f:
            f.write(newkey)
        self.lastkey = newkey