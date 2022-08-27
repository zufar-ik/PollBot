import random
import sqlite3
import asyncio
from itertools import groupby

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data.config import ADMINS
from loader import db, bot
from loader import dp


@dp.message_handler(commands='dell')
async def me(message: types.Message):
    for i in range(0, 10):
        tops = await db.all_tops()
        number = random.randint(0,int(len(tops)))
        print(number)
        poll_db = await db.all_quest(name_id=int(tops[0]['name'])) # для рандома вопросов
        print(len(poll_db[0]['img']))
        # poll_db = await db.all_quest(name_id=int(tops[]['id']))  # в зависимости от индекс выводится нужный топик
        # Вопрос № 1
        answer_db = await db.where_answer(
            question_id=int(poll_db[i]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу

        answer_true = []
        answer = []
        for i in answer_db:
            answer_true.append(f"{i['options']}:{i['correct_option']}")
        for i in answer_db:
            answer.append(f'{i["options"]}')
        true = next((i for i, s in enumerate(answer_true) if "True" in s), None)

        if (poll_db[i]['img']) == '':
            await message.answer_photo(photo=open(f'backends/{poll_db[i]["img"]}', 'rb'), )
        elif (poll_db[i]['video_gif']) == '':
            await message.answer_video(video=open(f'backends/{poll_db[i]["video_gif"]}', 'rb'))
        else:
            pass

        await message.bot.send_poll(chat_id='-714984123', question=poll_db[i]['question'], options=answer,
                                    is_anonymous=poll_db[i]['is_anonymous'],
                                    correct_option_id=true, type=poll_db[i]['type'],
                                    explanation=poll_db[i]['explanation'],
                                    open_period=poll_db[i]['open_period'], protect_content=True)

        @dp.poll_answer_handler()
        async def poll_answer(poll_answer: types.PollAnswer):
            answer_ids = poll_answer
            point = 0
            if int(true) == int(answer_ids['option_ids'][0]):
                point += 1

            else:
                point = 0
            await db.user_answer_info(tg_id=int(answer_ids['user']['id']), name=answer_ids['user']['first_name'],
                                      poll_id=answer_ids['poll_id'], true_option=true,
                                      answer=str(answer_ids['option_ids'][0]), point=point)

        await asyncio.sleep(poll_db[i]['open_period'])
