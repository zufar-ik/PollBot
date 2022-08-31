import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db

url = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Поделиться ссылкой', url=f'https://t.me/Avtotestbotuz_bot?startgroup')]
    ]
)


async def make_course():
    type = InlineKeyboardMarkup(row_width=2)
    for i in await db.get_all_course():
        type.insert(InlineKeyboardButton(text=f'{i["type"]}', callback_data=f'{i["type"]}:call'))
    return type
