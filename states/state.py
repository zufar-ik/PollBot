from aiogram.dispatcher.filters.state import StatesGroup, State


class Reklama(StatesGroup):
    reklama = State()

class Quest(StatesGroup):
    question = State()
    stop = State()

