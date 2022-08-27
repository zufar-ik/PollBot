import logging
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from loader import db


url = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Поделиться ссылкой',url=f'https://t.me/Avtotestbotuz_bot?startgroup')]
    ]
)