import asyncio
import json
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from nats.aio.msg import Msg as MsgNats
from telebot.apihelper import ApiTelegramException

from model import Env, MsgEvents
from util import nats_connect, load_yaml

env = load_yaml("./config.yaml", Env)

bot = Bot(env.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


async def message_handler_telegram(message: MsgNats):
    """Takes a message from nats and sends it to telegram."""

    msg = MsgEvents(**json.loads(message.data.decode()))
    logging.debug("tw.events > %s", msg)
    try:
        await bot.send_message(
            env.chat_id,
            f"{msg.server_name}: `{msg.rcon}`",
            message_thread_id=env.message_thread_id
        )
    except ApiTelegramException:
        logging.debug("ApiTelegramException occurred")


async def main() -> None:
    bot.ns, bot.js = await nats_connect(env)
    await bot.js.subscribe(
        "tw.events",
        "moderator_bot",
        cb=message_handler_telegram
    )
    logging.info("nats js subscribe \"tw.events\"")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    logging.basicConfig(
        level=getattr(logging, env.log_level.upper()),
        format='%(asctime)s:%(levelname)s:%(name)s: %(message)s',
    )
    asyncio.run(main())