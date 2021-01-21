from aiogram import (
    Bot, Dispatcher, executor, types
)
import asyncio, os
import aioschedule
import json

bot = Bot(token = '1549669090:AAEtDBdzYf_le6Dvx_DRNiO2qtBOIeG9lAM')
# 1011547803:AAGVi0ilCkXixUF5--uArNYa5oy0oW3p5_k
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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
