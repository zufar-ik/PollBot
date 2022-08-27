import asyncio

import pandas as pd
from aiogram import types
from aiogram.dispatcher import FSMContext

from data.config import ADMINS
from loader import dp, db, bot
from states.state import Reklama


@dp.message_handler(text="/allusers", user_id=ADMINS)
async def get_all_users(message: types.Message):
    users = await db.select_all_users()
    id = []
    name = []
    for user in users:
        id.append(user[0])
        name.append(user[1])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)

@dp.message_handler(commands='allgroup',user_id=ADMINS)
async def get_all_group(message: types.Message):
    group = await db.select_all_group()
    id = []
    name = []
    for groups in group:
        id.append(groups['group_id'])
        name.append(groups['name'])
    data = {
        "Telegram ID": id,
        "Name": name
    }
    pd.options.display.max_rows = 10000
    df = pd.DataFrame(data)
    if len(df) > 50:
        for x in range(0, len(df), 50):
            await bot.send_message(message.chat.id, df[x:x + 50])
    else:
       await bot.send_message(message.chat.id, df)
@dp.message_handler(text="/reklama", user_id=ADMINS)
async def send_ad_to_all(message: types.Message):
    await message.answer("Введите текст рекламы")
    await Reklama.reklama.set()


@dp.message_handler(state=Reklama.reklama)
async def send_ad_to_all(message: types.Message, state: FSMContext):
    reklama_text = message.text
    await state.update_data(
        {"reklama": reklama_text}
    )
    data = await state.get_data()
    reklama = data.get("reklama")
    group = await db.select_all_group()
    for groups in group:
        group_id = groups['group_id']
        await bot.send_message(chat_id=group_id, text=reklama)
        await asyncio.sleep(0.05)
    await state.finish()
