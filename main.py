import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.bot.routes import bot_router
from app.handlers.registration.routes import registration_router
from app.handlers.start.routes import main_router
from app.not_found import not_found_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


async def main():
    bot = Bot(token="6769418823:AAH_MFucMQuD_kINAtJpzG_U_nwC6D1_8O0")

    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(registration_router)
    dp.include_router(bot_router)
    dp.include_router(not_found_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot Stopped")
