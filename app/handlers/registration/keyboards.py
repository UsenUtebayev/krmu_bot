from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

get_number = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Отправьте ваш номер телефона", request_contact=True)]],
                                 resize_keyboard=True, one_time_keyboard=True)

position_texts = ["Студент", "Преподователь", "Менеджер"]
position_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=x) for x in position_texts]
], resize_keyboard=True, one_time_keyboard=True)

degree_texts = ['Бакалавр', 'Магистрант']
degree_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text=x) for x in degree_texts]
], resize_keyboard=True, one_time_keyboard=True)
