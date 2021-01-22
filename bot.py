from aiogram import (
    Bot, Dispatcher, executor, types
)
import asyncio, os
import aioschedule
import json
import aiohttp
import os

from aiohttp import web
from urllib.parse import urljoin
from aiogram.dispatcher.webhook import get_new_configured_app
from aiogram.utils import context

TOKEN = '1549669090:AAEtDBdzYf_le6Dvx_DRNiO2qtBOIeG9lAM'

WEBHOOK_HOST = 'https://simpleloopbot.herokuapp.com/'
WEBHOOK_URL_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = urljoin(WEBHOOK_HOST, WEBHOOK_URL_PATH)

bot = Bot(token = TOKEN) # 1549669090:AAEtDBdzYf_le6Dvx_DRNiO2qtBOIeG9lAM
bot_name = 'LoopBot'
dp = Dispatcher(bot)

async def read_setting() -> None:
    with open('setting.json', 'r', encoding='utf-8') as out:
        return json.load(out)

async def write_setting(setting: dict) -> None:
    with open('setting.json', 'w', encoding='utf-8') as out:
        out.write(json.dumps(setting, indent=2, sort_keys=True))   

@dp.message_handler(commands = ['start'])
async def start_bot(message: types.Message):
    try:
        setting = await read_setting()
        setting['message'] = message.text.split('-')[1][1:]

        await write_setting(setting)
        await bot.send_message(message.from_user.id, "OK!")
    
    except Exception as error:
        pass

@dp.message_handler(commands = ['stop'])
async def stop_bot_loop(message: types.Message):
    setting = await read_setting()
    setting['is_block'] = True

    await write_setting(setting)
    await bot.send_message(message.from_user.id, "Stop Bot!")

async def send_message() -> None:
    setting = await read_setting()
    if not setting['is_block']:
        await bot.send_message("@naedinesnisso", setting['message'])

async def sheduler():
    setting = await read_setting()
    aioschedule.every().day.at(setting['time']).do(send_message)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

async def on_startup(x):
    asyncio.create_task(sheduler())
    await bot.delete_webhook()
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(dp):
    pass

if __name__ == '__main__':

    try:
        app = get_new_configured_app(dispatcher=dp, path=WEBHOOK_URL_PATH)
        app.on_startup.append(on_startup)
        app.on_shutdown.append(on_shutdown)
        dp.loop.set_task_factory(context.task_factory)
        web.run_app(app, host='0.0.0.0', port=os.environ.get('PORT'))
    except Exception as error:
        print(error.__class__.__name__, error)
