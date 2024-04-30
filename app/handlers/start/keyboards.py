from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_text = [
    "Зарегистрироваться", "Помощь", "FAQ об университете", "Контакты университета"
]

buttons = [KeyboardButton(text=x) for x in button_text]

main = ReplyKeyboardMarkup(keyboard=
[
    buttons
], resize_keyboard=True, input_field_placeholder='Выберите дальнеейшее действие', one_time_keyboard=True)
