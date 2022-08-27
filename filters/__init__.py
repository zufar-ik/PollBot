from aiogram import Dispatcher

from loader import dp
from .is_admin import AdminFilter
from .group import IsGroup
from .private import IsPrivate
from .users import UserFilters


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(IsGroup)
    dp.filters_factory.bind(IsPrivate)
    dp.filters_factory.bind(UserFilters)
