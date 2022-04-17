from bs4 import BeautifulSoup
import requests


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
}

r = requests.get('https://www.gazeta.uz/oz/economy/', headers=headers)
soap = BeautifulSoup(r.content, 'lxml')