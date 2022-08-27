import random
import asyncio
from itertools import groupby

import aiogram
import asyncpg
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart

from keyboards.inline.menu_keyboards import url
from loader import db, bot
from loader import dp
from filters import IsGroup, IsPrivate, AdminFilter, UserFilters
from states.state import Quest


@dp.message_handler(IsPrivate(), commands='poll')
async def poll(message: types.Message):
    await message.answer('Не будет ли тебе скучно одному решать тесты!?\n'
                         'Лучше добавь меня к себе в группу чтобы играть с друзьями!', reply_markup=url)


@dp.message_handler(IsGroup(), CommandStart())
async def poll(message: types.Message):
    await message.answer('Мои команды\n\n'
                         '/poll - Запуск теста!')


@dp.message_handler(IsGroup(), commands='poll')
async def poll(message: types.Message, state: FSMContext):
    try:
        await db.add_group(chat_id=message.chat.id,name=message.chat.full_name)
    except asyncpg.exceptions.UniqueViolationError:
        pass
    await Quest.question.set()
    msg = []
    top = []
    tops = await db.all_tops()
    for i in tops:
        top.append(i['id'])
    number = random.choice(top)
    poll_db = await db.all_quest(name_id=int(number))  # для рандома вопросов
    # Вопрос № 1
    answer_db = await db.where_answer(
        question_id=int(poll_db[0]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')


    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[0]['img']) >= 1:
        photo1 = await message.answer_photo(photo=open(f'backends/{poll_db[0]["img"]}', 'rb'), )
        msg.append(photo1.message_id)
    elif len(poll_db[0]['video_gif']) >= 1:
        video1 = await message.answer_video(video=open(f'backends/{poll_db[0]["video_gif"]}', 'rb'))
        msg.append(video1.message_id)
    else:
        pass

    try:
        msg1 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[0]['question'], options=answer,
                                           is_anonymous=poll_db[0]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[0]['type'],
                                           explanation=poll_db[0]['explanation'],
                                           open_period=poll_db[0]['open_period'], protect_content=True)
        msg.append(msg1.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg1 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[0]['question'], options=result,
                                           is_anonymous=poll_db[0]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[0]['type'],
                                           explanation=poll_db[0]['explanation'],
                                           open_period=poll_db[0]['open_period'], protect_content=True)
        msg.append(msg1.message_id)
        MSG1 = await message.answer(poll_db[0]['answer'])
        msg.append(MSG1.message_id)
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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[0]['open_period'])

    # Вопрос № 2
    answer_db = await db.where_answer(
        question_id=int(poll_db[1]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[1]['img']) >= 1:
        photo2 = await message.answer_photo(photo=open(f'backends/{poll_db[1]["img"]}', 'rb'), )
        msg.append(photo2.message_id)

    elif len(poll_db[1]['video_gif']) >= 1:
        video2 = await message.answer_video(video=open(f'backends/{poll_db[1]["video_gif"]}', 'rb'))
        msg.append(video2.message_id)
    else:
        pass

    try:
        msg2 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[1]['question'], options=answer,
                                           is_anonymous=poll_db[1]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[1]['type'],
                                           explanation=poll_db[1]['explanation'],
                                           open_period=poll_db[1]['open_period'], protect_content=True)
        msg.append(msg2.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg2 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[1]['question'], options=result,
                                           is_anonymous=poll_db[1]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[1]['type'],
                                           explanation=poll_db[1]['explanation'],
                                           open_period=poll_db[1]['open_period'], protect_content=True)
        msg.append(msg2.message_id)
        MSG2 = await message.answer(poll_db[1]['answer'])
        msg.append(MSG2.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[1]['open_period'])

    # Вопрос № 3
    answer_db = await db.where_answer(
        question_id=int(poll_db[2]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[2]['img']) >= 1:
        photo3 = await message.answer_photo(photo=open(f'backends/{poll_db[2]["img"]}', 'rb'), )
        msg.append(photo3.message_id)

    elif len(poll_db[2]['video_gif']) >= 1:
        video3 = await message.answer_video(video=open(f'backends/{poll_db[2]["video_gif"]}', 'rb'))
        msg.append(video3.message_id)

    else:
        pass

    try:
        msg3 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[2]['question'], options=answer,
                                           is_anonymous=poll_db[2]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[2]['type'],
                                           explanation=poll_db[2]['explanation'],
                                           open_period=poll_db[2]['open_period'], protect_content=True)
        msg.append(msg3.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg3 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[2]['question'], options=result,
                                           is_anonymous=poll_db[2]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[2]['type'],
                                           explanation=poll_db[2]['explanation'],
                                           open_period=poll_db[2]['open_period'], protect_content=True)
        msg.append(msg3.message_id)
        MSG3 = await message.answer(poll_db[2]['answer'])
        msg.append(MSG3.message_id)

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
                                      answer=str(answer_ids['option_ids'][0]), point=point,
                                      chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[2]['open_period'])

    # Вопрос № 4
    answer_db = await db.where_answer(
        question_id=int(poll_db[3]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[3]['img']) >= 1:
        photo4 = await message.answer_photo(photo=open(f'backends/{poll_db[3]["img"]}', 'rb'), )
        msg.append(photo4.message_id)

    elif len(poll_db[3]['video_gif']) >= 1:
        video4 = await message.answer_video(video=open(f'backends/{poll_db[3]["video_gif"]}', 'rb'))
        msg.append(video4.message_id)

    else:
        pass

    try:
        msg4 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[3]['question'], options=answer,
                                           is_anonymous=poll_db[3]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[3]['type'],
                                           explanation=poll_db[3]['explanation'],
                                           open_period=poll_db[3]['open_period'], protect_content=True)
        msg.append(msg4.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg4 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[3]['question'], options=result,
                                           is_anonymous=poll_db[3]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[3]['type'],
                                           explanation=poll_db[3]['explanation'],
                                           open_period=poll_db[3]['open_period'], protect_content=True)
        msg.append(msg4.message_id)
        MSG4 = await message.answer(poll_db[3]['answer'])
        msg.append(MSG4.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[3]['open_period'])

    # Вопрос № 5
    answer_db = await db.where_answer(
        question_id=int(poll_db[4]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[4]['img']) >= 1:
        photo5 = await message.answer_photo(photo=open(f'backends/{poll_db[4]["img"]}', 'rb'), )
        msg.append(photo5.message_id)

    elif len(poll_db[4]['video_gif']) >= 1:
        video5 = await message.answer_video(video=open(f'backends/{poll_db[4]["video_gif"]}', 'rb'))
        msg.append(video5.message_id)

    else:
        pass

    try:
        msg5 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[4]['question'], options=answer,
                                           is_anonymous=poll_db[4]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[4]['type'],
                                           explanation=poll_db[4]['explanation'],
                                           open_period=poll_db[4]['open_period'], protect_content=True)
        msg.append(msg5.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg5 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[4]['question'], options=answer,
                                           is_anonymous=poll_db[4]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[4]['type'],
                                           explanation=poll_db[4]['explanation'],
                                           open_period=poll_db[4]['open_period'], protect_content=True)
        msg.append(msg5.message_id)
        MSG5 = await message.answer(poll_db[4]['answer'])
        msg.append(MSG5.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[4]['open_period'])

    # Вопрос № 6
    NUM = 5
    answer_db = await db.where_answer(
        question_id=int(poll_db[NUM]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')

    result = [x.split('.')[0] for x in answer]
    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[NUM]['img']) >= 1:
        photo6 = await message.answer_photo(photo=open(f'backends/{poll_db[NUM]["img"]}', 'rb'), )
        msg.append(photo6.message_id)

    elif len(poll_db[NUM]['video_gif']) >= 1:
        video6 = await message.answer_video(video=open(f'backends/{poll_db[NUM]["video_gif"]}', 'rb'))
        msg.append(video6.message_id)

    else:
        pass

    try:
        msg6 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=answer,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg6.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg6 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=result,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg6.message_id)
        MSG6 = await message.answer(poll_db[NUM]['answer'])
        msg.append(MSG6.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[NUM]['open_period'])

    # Вопрос № 7
    NUM = 6
    answer_db = await db.where_answer(
        question_id=int(poll_db[NUM]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[NUM]['img']) >= 1:
        photo7 = await message.answer_photo(photo=open(f'backends/{poll_db[NUM]["img"]}', 'rb'), )
        msg.append(photo7.message_id)

    elif len(poll_db[NUM]['video_gif']) >= 1:
        video7 = await message.answer_video(video=open(f'backends/{poll_db[NUM]["video_gif"]}', 'rb'))
        msg.append(video7.message_id)

    else:
        pass

    try:
        msg7 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=answer,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg7.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg7 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=result,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg7.message_id)
        MSG7 = await message.answer(poll_db[NUM]['answer'])
        msg.append(MSG7.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[NUM]['open_period'])

    # Вопрос № 8
    NUM = 7
    answer_db = await db.where_answer(
        question_id=int(poll_db[NUM]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]
    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[NUM]['img']) >= 1:
        photo8 = await message.answer_photo(photo=open(f'backends/{poll_db[NUM]["img"]}', 'rb'), )
        msg.append(photo8.message_id)

    elif len(poll_db[NUM]['video_gif']) >= 1:
        video8 = await message.answer_video(video=open(f'backends/{poll_db[NUM]["video_gif"]}', 'rb'))
        msg.append(video8.message_id)

    else:
        pass

    try:
        msg8 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=answer,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg8.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg8 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=result,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg8.message_id)
        MSG8 = await message.answer(poll_db[NUM]['answer'])
        msg.append(MSG8.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[NUM]['open_period'])

    # Вопрос № 9
    NUM = 8
    answer_db = await db.where_answer(
        question_id=int(poll_db[NUM]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]

    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[NUM]['img']) >= 1:
        photo9 = await message.answer_photo(photo=open(f'backends/{poll_db[NUM]["img"]}', 'rb'), )
        msg.append(photo9.message_id)

    elif len(poll_db[NUM]['video_gif']) >= 1:
        video9 = await message.answer_video(video=open(f'backends/{poll_db[NUM]["video_gif"]}', 'rb'))
        msg.append(video9.message_id)

    else:
        pass

    try:
        msg9 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=answer,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg9.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg9 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=result,
                                           is_anonymous=poll_db[NUM]['is_anonymous'],
                                           correct_option_id=true, type=poll_db[NUM]['type'],
                                           explanation=poll_db[NUM]['explanation'],
                                           open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg9.message_id)
        MSG9 = await message.answer(poll_db[NUM]['answer'])
        msg.append(MSG9.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[NUM]['open_period'])

    # Вопрос № 10
    NUM = 9
    answer_db = await db.where_answer(
        question_id=int(poll_db[NUM]['id']))  # с каждым вопросом увеличивать число 0 - 9 по индексу
    answer_true = []
    answer = []
    for i in answer_db:
        answer_true.append(f"{i['options']}:{i['correct_option']}")
    for i in answer_db:
        answer.append(f'{i["options"]}')
    result = [x.split('.')[0] for x in answer]
    true = next((i for i, s in enumerate(answer_true) if "True" in s), None)
    if len(poll_db[NUM]['img']) >= 1:
        photo10 = await message.answer_photo(photo=open(f'backends/{poll_db[NUM]["img"]}', 'rb'), )
        msg.append(photo10.message_id)

    elif len(poll_db[NUM]['video_gif']) >= 1:
        video10 = await message.answer_video(video=open(f'backends/{poll_db[NUM]["video_gif"]}', 'rb'))
        msg.append(video10.message_id)

    else:
        pass

    try:
        msg10 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=answer,
                                            is_anonymous=poll_db[NUM]['is_anonymous'],
                                            correct_option_id=true, type=poll_db[NUM]['type'],
                                            explanation=poll_db[NUM]['explanation'],
                                            open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg10.message_id)
    except aiogram.utils.exceptions.PollOptionsLengthTooLong:
        msg10 = await message.bot.send_poll(chat_id=message.chat.id, question=poll_db[NUM]['question'], options=result,
                                            is_anonymous=poll_db[NUM]['is_anonymous'],
                                            correct_option_id=true, type=poll_db[NUM]['type'],
                                            explanation=poll_db[NUM]['explanation'],
                                            open_period=poll_db[NUM]['open_period'], protect_content=True)
        msg.append(msg10.message_id)
        MSG10 = await message.answer(poll_db[NUM]['answer'])
        msg.append(MSG10.message_id)

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
                                  answer=str(answer_ids['option_ids'][0]), point=point, chat_id=str(message.chat.id))

    await asyncio.sleep(poll_db[NUM]['open_period'])

    user_db = []
    user = await db.views_user_answer(chat_id=str(message.chat.id))
    for i in user:
        if f"{i['tg_id']}:{i['name']}" in user_db:
            pass
        else:
            user_db.append(f"{i['tg_id']}:{i['name']}")
    ids = [x.split(':')[0] for x in user_db]
    liss = []
    for i in ids:
        user_where = await db.views_user_answer(tg_id=int(i), chat_id=str(message.chat.id))
        for i in user_where:
            liss.append(f"{i['tg_id']}:{i['point']}")
    liss = [obj.split(':') for obj in liss]
    result = {}
    for k, g in groupby(sorted(liss), key=lambda x: x[0]):
        result[k] = sum(int(v) for _, v in g)
    result = dict(sorted(result.items(), key=lambda obj: obj[1], reverse=True))
    liss = ([f'{k}:{v}' for k, v in result.items()])
    msge = 'Таблица лидеров!\n\n'
    count = 0
    print(liss)
    for i in liss:
        count += 1
        use_name = await db.views_user_answer(tg_id=int(i.split(":")[0]), chat_id=str(message.chat.id))
        msge += f'{count}. <a href="tg://user?id={i.split(":")[0]}">{use_name[0]["name"]}</a> - {i.split(":")[1]} из 10\n\n'

    await message.bot.send_message(chat_id=message.chat.id, text=msge)
    for i in msg:
        await bot.delete_message(chat_id=message.chat.id, message_id=i)
    await db.drop_users_answer(chat_id=str(message.chat.id))
    await state.finish()


@dp.message_handler(IsGroup(), UserFilters(), commands='poll')
async def poll(message: types.Message):
    await message.answer('Попроси админа группы чтобы он запустил тест!')


