import logging
from aiogram import Bot, Dispatcher

from modules.bot.handlers import router
from modules.bot.exceptions import errors_router


dp = Dispatcher()


async def start_bot(bot: Bot):
    dp.include_routers(router, errors_router)

    await dp.start_polling(bot, allowed_updates=["*"])
    
    logging.info("Bot started")
