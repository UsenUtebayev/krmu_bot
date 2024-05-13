from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboards = [
    'Начать диалог с ботом',
    'Узнать расписание'

]

main_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=x) for x in keyboards]
], resize_keyboard=True, one_time_keyboard=True)
