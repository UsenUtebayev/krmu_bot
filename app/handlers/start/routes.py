from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

import app.handlers.start.keyboards as kb
from app.database.requests import set_user
from app.handlers.main.keyboards import main_keyboard
from app.template_enviroment import env

main_router = Router()


@main_router.message(CommandStart())
async def start(message: Message):
    user = set_user(message.from_user.id)
    template = env.get_template("start.txt")
    plaintext = template.render(
        user=user,
    )
    if not user:
        await message.answer(plaintext, reply_markup=kb.main)
    else:
        await message.answer(plaintext, reply_markup=main_keyboard)


@main_router.message(F.text == "FAQ об университете")
async def faq(message: Message):
    template = env.get_template("faq.txt")
    plaintext = template.render()
    await message.answer(plaintext, reply_markup=kb.main, parse_mode="Markdown")


@main_router.message(F.text == "Контакты университета")
async def contacts(message: Message):
    template = env.get_template("contacts.txt")
    plaintext = template.render()
    await message.answer(plaintext, reply_markup=kb.main)
