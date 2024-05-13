import re

from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.handlers.bot.buttons import bot_buttons
from app.handlers.bot.states import BotStates
from app.handlers.bot.utils import ready_prompt, model, REFACTOR_REGEX
from app.handlers.main.keyboards import main_keyboard

bot_router = Router()


@bot_router.message(F.text == "Начать диалог с ботом")
async def bot(message: Message, state: FSMContext):
    await message.answer("Начат диалог с ботом для выхода используйте команду /end_bot_dialog или нажмите кнопку",
                         reply_markup=bot_buttons)
    await state.set_state(BotStates.working)


@bot_router.message(BotStates.working)
async def bot_working(message: Message, state: FSMContext):
    if message.text == "Закончить диалог с ботом" or message.text == "/end_bot_dialog":
        await state.clear()
        await message.answer("Диалог с ботом закончен!", reply_markup=main_keyboard)
    else:
        sended_msg = await message.reply("Бот отвечает...")
        chat = model.start_chat()
        text_response = []
        responses = chat.send_message(f"{ready_prompt} - это твоя конфигурация а ниже запрос пользвателя"
                                      f"{message.text}", stream=True)
        for chunk in responses:
            text_response.append(chunk.text)
        response_text = re.sub(REFACTOR_REGEX, lambda t: "\\" + t.group(), "".join(text_response))
        await sended_msg.edit_text(response_text, parse_mode="MarkdownV2")
        await state.set_state(BotStates.working)
