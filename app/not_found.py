from aiogram import Router
from aiogram.types import Message

not_found_router = Router()


@not_found_router.message()
async def not_found(message: Message):
    await message.reply("Не найдена такая команда")
