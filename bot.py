from aiogram import executor
import aioschedule
import asyncio

from datetime import datetime

from .config import *
from .investing_parser import InvestingComParser
from .denotations import importances, flags
from .investing_news_parser import InvestingNewsParser
from .crypto_news_parser import CryptoNewsParser


loop = asyncio.get_event_loop()

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
    now = datetime.now()
    remind_time = datetime.strptime(f'{now.date()} {time}:00', '%Y-%m-%d %H:%M:%S')
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


async def scheduler():
    aioschedule.every().day.at("00:00").do(send_today_events)
    aioschedule.every(15).minutes.do(investing_send_news)
    aioschedule.every(4).hours.do(crypto_send_news)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(10)


async def on_startup(_):
    await asyncio.create_task(scheduler())


executor.start_polling(dp, skip_updates=True, on_startup=crypto_send_news)