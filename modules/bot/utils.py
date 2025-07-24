from typing import Callable
from aiogram.filters import CommandObject

from modules.bot.exceptions import IncorrectArgsError


def parse_args(command: CommandObject, min_amount: int, func: Callable = None) -> list[str]:
    if not min_amount and command.args is None:
        return []

    if command.args is None:
        raise IncorrectArgsError(command.text)

    args = command.args.split()

    if len(args) < min_amount:
        raise IncorrectArgsError(command.text)

    return args if func is None else list(map(func, args))
