from aiogram import executor
import asyncio

from datetime import datetime

from .config import *
from .investing_parser import InvestingComParser
from .cnbc_parser import CnbcParser
from .denotations import importances, flags


loop = asyncio.get_event_loop()

async def reminder(event):
    currency = event['currency']
    country = event['country']
    importance = importances[event['importance']]
    name = event['event_name']
    previous = event['previous']
    text = f'<b>15min</b> {flags[country]} {currency} {importance} {name} {previous}\n\n'
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


async def send_news(_):
    parser = CnbcParser()
    news = parser.get_news()
    for post in news:
        title = post['title']
        link = post['link']
        text = f'{title}\n<a href="{link}">Ko\'rish</a>'
        await bot.send_message('@ufinancenews', text, parse_mode='html')

executor.start_polling(dp, skip_updates=True, on_startup=send_news)