from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

bot_buttons = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Закончить диалог с ботом')]
],resize_keyboard=True, one_time_keyboard=True)