from bs4 import BeautifulSoup
import requests

from .translator import translator


class InvestingComParser():

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
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

    r = requests.get('https://www.investing.com/economic-calendar/', headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    date = None
    events = []

    def __init__(self):

        self.date = self.soup.find('td', class_='theDay')
        self.events = self.soup.find_all('tr', class_='js-event-item')

    def get_event_details_by_html(self, event):
        event_id = event['id']
        time = event.find('td', class_='js-time')
        currency = event.find('td', class_='flagCur')
        country = currency.find('span')['title']
        importance = event.find('td', class_='sentiment')['title']
        event_name = event.find('td', class_='event')
        actual = event.find('td', class_='act')
        forecast = event.find('td', class_='fore')
        previous = event.find('td', class_='prev')
        return {
            'event_id': event_id, 
            'time': time.text, 
            'currency': currency.text[2:], 
            'country': country, 
            'importance': importance,
            'event_name': translator.translate(event_name.text, dest='uz').text,
            'actual': actual.text,
            'forecast': forecast.text,
            'previous': previous.text
        }

    def events_details(self):
        events_details = []
        for event in self.events:
            events_details.append(self.get_event_details_by_html(event))
        return events_details
