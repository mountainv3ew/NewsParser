import asyncio
import logging

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter, TelegramBadRequest
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from database.database import async_session
from database.keywords import get_user_keywords
from database.subscriptions import get_all_subscriptions
from models.data.Telegram import TelegramMessage


class Pusher:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.message_queue = asyncio.Queue()
        self.message_queue_enabled = True

        self.subscriptions_dict = {}

        self.scheduler = AsyncIOScheduler()
        self.scheduler.add_job(
            self.update_subscriptions_dict, 'interval', seconds=10)

    async def new_post(self, username: str, text: str):
        text = f"Channel @{username} wrote:\n" + text
        texts = [text[i:i+4096] for i in range(0, len(text), 4096)]

        if self.subscriptions_dict.get(username) is None:
            logging.error("Channel username is not in database")
            return

        for user_id in self.subscriptions_dict.get(username):
            async with async_session.begin() as sess:
                keywords = await get_user_keywords(sess, user_id)
            if not any(keyword.lower() in text.lower() for keyword in keywords for text in texts):
                break
            for text in texts:
                await self.message_queue.put(TelegramMessage(user_id=user_id, text=text))

    async def update_subscriptions_dict(self):
        async with async_session.begin() as sess:
            subscriptions = await get_all_subscriptions(sess)

        subscriptions_dict: dict[str, set] = {}
        for subscription in subscriptions:
            if subscriptions_dict.get(subscription.channel) is None:
                subscriptions_dict[subscription.channel] = {
                    subscription.user_id}
            else:
                subscriptions_dict[subscription.channel].add(
                    subscription.user_id)

        self.subscriptions_dict = subscriptions_dict

    async def start_queue_processing(self):
        self.scheduler.start()

        logging.info("Start pusher")
        
        while self.message_queue:
            msg: TelegramMessage = await self.message_queue.get()

            try:
                await self.bot.send_message(msg.user_id, msg.text)
            except TelegramRetryAfter:
                await asyncio.sleep(60)
                continue
            except TelegramBadRequest as e:
                logging.error(f"Pusher error: {e}")

            self.message_queue.task_done()

    def stop_queue_processing(self):
        self.message_queue_enable = False
