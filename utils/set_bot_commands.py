from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Старт бота"),
            types.BotCommand("help", "Помощь"),
            types.BotCommand('poll','Вопросы')
        ]
    )
