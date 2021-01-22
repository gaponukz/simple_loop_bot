from aiogram.utils.executor import start_webhook
from aiogram.dispatcher import Dispatcher
from aiogram import Bot, types

import asyncio, os
import aioschedule
import json
import logging

TOKEN = "1549669090:AAEtDBdzYf_le6Dvx_DRNiO2qtBOIeG9lAM"

WEBHOOK_HOST = 'https://simpleloopbot.herokuapp.com'
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.environ.get('PORT')

bot = Bot(token = TOKEN)
bot_name = 'LoopBot'
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

async def read_setting() -> None:
    with open('setting.json', 'r', encoding='utf-8') as out:
        return json.load(out)

async def write_setting(setting: dict) -> None:
    with open('setting.json', 'w', encoding='utf-8') as out:
        out.write(json.dumps(setting, indent=2, sort_keys=True))   

@dp.message_handler(commands = ['start'])
async def start_bot(message: types.Message):
    setting = await read_setting()
    setting['message'] = message.text.split('-')[1][1:]

    await write_setting(setting)
    await bot.send_message(message.from_user.id, "OK!")

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

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    # asyncio.create_task(sheduler())

async def on_shutdown(dp):
    pass

if __name__ == '__main__':
    start_webhook(
        dispatcher = dp,
        webhook_path = WEBHOOK_PATH,
        on_startup = on_startup,
        on_shutdown = on_shutdown,
        host = WEBAPP_HOST,
        port = WEBAPP_PORT
    )
