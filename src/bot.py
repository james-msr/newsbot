from aiogram import executor
import aioschedule
import asyncio

import datetime

from .config import *
from .parsers.investing_parser import InvestingComParser
from .denotations import importances, flags
from .parsers.investing_news_parser import InvestingNewsParser
from .parsers.crypto_news_parser import CryptoNewsParser
from .parsers.gazeta_news_parser import GazetaNewsParser
from .parsers.kunuz_news_parser import KunuzNewsParser



async def reminder(event):
    time = event['time']
    currency = event['currency']
    country = event['country']
    importance = importances[event['importance']]
    name = event['event_name']
    previous = event['previous']
    text = f'<b>{time}</b> {flags[country]} {currency} {importance} {name} {previous}\n\n'
    await bot.send_message('@ufinancenews', text, parse_mode='html')


def my_func(event):
    asyncio.ensure_future(reminder(event))


async def event_reminder(time, event):
    loop = asyncio.get_event_loop()
    now = datetime.datetime.now()
    remind_time = datetime.datetime.strptime(f'{now.date()} {time}:00', '%Y-%m-%d %H:%M:%S')
    diff = remind_time - now
    delay = diff.seconds - 900
    loop.call_later(delay, my_func, event)


async def send_today_events():
    parser = InvestingComParser()
    events = parser.events_details()
    text = ''
    for event in events:
        time = event['time']
        currency = event['currency']
        country = event['country']
        importance = importances[event['importance']]
        name = event['event_name']
        previous = event['previous']
        text += f'<b>{time}</b> {flags[country]} {currency} {importance} {name} {previous}\n\n'
        await event_reminder(time, event)
    await bot.send_message('@ufinancenews', text, parse_mode='html')


async def investing_send_news():
    parser = InvestingNewsParser()
    news = parser.get_news()
    if(news):
        news.reverse()
        text = ''
        for post in news:
            title = post['title']
            content = post['content']
            text = f'<b>{title}</b>'
            newkey = post['key']
            await bot.send_photo('@ufinancenews', post['photo_url'], text, parse_mode='html')
            await parser.update_lastkey(newkey)
            await asyncio.sleep(30)


async def crypto_send_news():
    parser = CryptoNewsParser()
    news = parser.get_news()
    if(news):
        news.reverse()
        text = ''
        for post in news:
            title = post['title']
            text = f'<b>{title}</b>'
            newkey = post['key']
            await bot.send_photo('@ufinancenews', post['photo_url'], text, parse_mode='html')
            await parser.update_lastkey(newkey)
            await asyncio.sleep(30)


async def gazeta_send_news():
    parser = GazetaNewsParser()
    news = parser.get_news()
    if(news):
        news.reverse()
        text = ''
        for post in news:
            title = post['title']
            url = post['more']
            text = f'<b>{title}</b>\n\n<a href="{url}">Ko\'proq</a>'
            newkey = post['key']
            await bot.send_message('@ufinancenews', text, parse_mode='html')
            await parser.update_lastkey(newkey)
            await asyncio.sleep(30)


async def kunuz_send_news():
    parser = KunuzNewsParser()
    news = parser.get_news()
    if(news):
        news.reverse()
        text = ''
        for post in news:
            title = post['title']
            url = post['more']
            text = f'<b>{title}</b>\n\n<a href="{url}">Ko\'proq</a>'
            newkey = post['key']
            await bot.send_message('@ufinancenews', text, parse_mode='html')
            await parser.update_lastkey(newkey)
            await asyncio.sleep(30)


async def send_news():
    await investing_send_news()
    await crypto_send_news()
    await gazeta_send_news()
    await kunuz_send_news()


async def scheduler():
    aioschedule.every().day.at(datetime.time(hour=00, tzinfo=datetime.timezone('Asia/Tashkent')))
    aioschedule.every(15).minutes.do(send_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(30)


async def on_startup(_):
    await asyncio.create_task(scheduler())


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)