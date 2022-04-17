from bs4 import BeautifulSoup
import requests
from .translator import translator

class InvestingNewsParser():
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-language': 'en-US,en;q=0.9,ru;q=0.8',
        'cache-control': 'max-age=0',
        'cookie': 'logglytrackingsession=b3c719b5-85f1-4c63-911f-ca35cd2f9d1a; PHPSESSID=6oc690ses8eehuc57ghhqgpnjq; adBlockerNewUserDomains=1647966349; StickySession=id.59686888297.614_www.investing.com; udid=01f10288820e250a69b183cb9b1aab78; protectedMedia=2; pms={"f":2,"s":2}; _ga=GA1.2.579635058.1647966355; G_ENABLED_IDPS=google; OB-USER-TOKEN=2566e053-362c-43cd-9bc5-4b12d6642a5a; r_p_s_n=1; _fbp=fb.1.1647966717773.1803098609; logglytrackingsession=2ae25e5c-9085-44ed-a85e-74b67539c9e9; geoC=UZ; gtmFired=OK; __cflb=02DiuGRugds2TUWHMkjZrtd2P76fwcs2jbSP8uyWLdKjA; _gid=GA1.2.1019582264.1648284433; hide_investing_pro_header_strip=1; adsFreeSalePopUp=3; smd=01f10288820e250a69b183cb9b1aab78-1648290493; __gads=ID=aa6d8dad8d6caf98:T=1648290510:S=ALNI_MaQmP-C-KpBXUj5gpaYAO3QHMpLEg; _pbjs_userid_consent_data=3524755945110770; cto_bundle=eJAUl194OFI0a2Y2ZzdYakx2cFZLTU1xd3A0MzA3cWZNd01xaVVCS0NFOFFLTDJUQ1hxY3psT28lMkZCTE82VTFic0xCMzVNcU1vSVEzdjhvYnhjTmNSaTBmWTBXMkNKTGVSc2xSc09TNlpZRk9XYXVpcW5OYmJubkUwZnh3bWYlMkZvTWZOanNlSG5OWjclMkJZS3hpWWRNaUJObHdHTWclM0QlM0Q; cto_bidid=owC0X19HdG9oOEs1dnZZaUZVNHZEaEJZdXRBdGZNMWNqNk5kMm0xQVZEOXVURTFhbzlQeCUyQjR3N203NVRJV2JjSHlOZmdmdXVYc3h2VkFuV0l5b0Z6MVFCbjJ5UzVjSHAlMkZ6WGtMN2FvSyUyQlo5TFNLbyUzRA; panoramaId_expiry=1648378772726; _cc_id=8153576ab6d815892d1ae40d63ce1e26; invpc=36; comment_notification_214177563=1; Adsfree_conversion_score=3; adsFreeSalePopUp358ee24fe9c41c741126f2559c8fd8a1=1; outbrain_cid_fetch=true; __cf_bm=lLCQ1OAJZsv15QIzy7zkGGJhO9A7iye2i5D63RAYy0E-1648294421-0-Ac5KGby8SEI1P3pYRSGiSfNY3YvUP97Ik9bcKney4vBDjM/VthfWcbBZBc0kee+wcgGiyYcQ7SODVlWvKSnVkdvYAMc3pcMvN8tmJhYTiNJPRJEu9XipkdGlIyzjQNvhvaVs1pk9bV6nCWl/4Uu2VCpVLfrtUz8KwF1jg9aeXuwg; nyxDorf=YGc1Z2M2ZSdiNjs0bj1mejduNmU%2FJmVmNjFvZQ%3D%3D; ses_id=ZSsyczI9ZGxiJm1rYjNlZmcyMGoxMWJnPTkzNjQwYHYyJjU7MWYzdTU6bCJkZ2R4YGI2ZT9hMWs0ZGdjNGNiPmVoMmMyN2Q5YmVtNWJiZWNnNTBoMTdiYj0%2BMzE0MWBsMjU1NTEwMz41YGwzZDhkYmByNio%2FezEgNGZnNzR1YiVlajJzMmJkOmI3bTRiZ2U2ZzIwOjE2YjQ9OzM2NDFgeDJ5',
        'referer': 'https://www.investing.com/economic-calendar/',
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

    r = requests.get('https://www.investing.com/news/latest-news', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    news_block = None
    news = []
    lastkey = ''
    

    def __init__(self):
        self.news_block = self.soup.find('div', class_='largeTitle')
        self.news = self.news_block.find_all('article', class_='js-article-item')

        try:
            with open('D:/Projects/newsbot/keys/investing_lastkey.txt', 'r') as f:
                self.lastkey = f.read()
        except:
            pass

    def get_post_by_html(self, post):
        title = post.find('div', class_='textDiv').find('a')
        key = post['data-id']
        try:
            details = self.get_post_details(title['href'])
            return {
            'title': translator.translate(title.text, dest='uz').text,
            'key': key,
            'photo_url': details['photo_url'],
            'content': translator.translate(details['content'], dest='uz').text
            }
        except:
            return {
                'error': 'Error'
            }

    def get_post_details(self, url):
        r = requests.get('https://www.investing.com/'+url, headers=self.headers)
        soup = BeautifulSoup(r.content, 'lxml')

        article = soup.find('div', class_='articlePage')
        img = article.find('img', id='carouselImage')

        return {
            'photo_url': img['src'],
            'content': article.text
        }

    def get_news(self):
        news_details = []
        for post in self.news:
            try:
                if post['data-id'] != self.lastkey:
                    details = self.get_post_by_html(post)
                    if 'error' in details:
                        continue
                    else:
                        news_details.append(details)
                else:
                    break
            except:
                continue
        return news_details

    async def update_lastkey(self, newkey):
        with open('D:/Projects/newsbot/keys/investing_lastkey.txt', 'w+') as f:
            f.write(newkey)
        self.lastkey = newkey