from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters.filters import BoundFilter

from config import config


@dataclass
class AdminFilter(BoundFilter):
    key = "is_admin"
    is_admin: bool

    async def check(self, message: types.Message) -> bool:
        return message.from_user.id == int(config['GENERAL']['ADMIN_ID']) or message.from_user.id == int(
            config['GENERAL']['MODERATOR_ID'])
