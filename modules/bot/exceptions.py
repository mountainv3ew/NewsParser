from aiogram import F, Router
from aiogram.filters import ExceptionTypeFilter
from aiogram.types import Message, ErrorEvent

from modules.bot.message_text import COMMAND_DOCS



class IncorrectArgsError(Exception):
    def __init__(self, command_name: str = ""):
        super().__init__()
        self.command_name = command_name


errors_router = Router()


@errors_router.error(ExceptionTypeFilter(IncorrectArgsError), F.update.message.as_("message"))
async def incorrect_args(event: ErrorEvent, message: Message):
    command_name = event.exception.__dict__.get('command_name')
    doc = COMMAND_DOCS.get(command_name or 'default', COMMAND_DOCS['default'])
    await message.reply(doc)
