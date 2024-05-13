from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from app.database.requests import get_all_major, add_user_information, get_user
from app.handlers.main.keyboards import main_keyboard
from app.handlers.registration.keyboards import position_keyboard, degree_keyboard, position_texts, degree_texts, \
    get_number
from app.handlers.registration.states import Registration
from app.handlers.registration.utils import fs_validator, ls_validator

registration_router = Router()


@registration_router.message(
    F.text == "Зарегистрироваться",
)
async def register(message: Message, state: FSMContext):
    user = get_user(tg_id=message.from_user.id)
    if user.is_questioned:
        await message.reply('Вы уже зарегистрированиы в системе! Для изменения своих данных введите /update_me')
        return
    await state.set_state(Registration.first_name)
    temp_keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=f"{message.from_user.first_name}")],
    ], resize_keyboard=True, one_time_keyboard=True)
    await message.answer("Пожалуйста напишите ваше имя", reply_markup=temp_keyboard)


@registration_router.message(Registration.first_name)
async def register_name(message: Message, state: FSMContext):
    if fs_validator(message.text):
        await state.update_data(first_name=message.text)
        await state.set_state(Registration.second_name)
        temp_keyboard = ReplyKeyboardMarkup(keyboard=[
            [KeyboardButton(text=f"{message.from_user.last_name}")],
        ], resize_keyboard=True, one_time_keyboard=True)
        temp_keyboard = temp_keyboard if message.from_user.last_name else None
        await message.answer("Пожалуйста напишите вашу фамилию", reply_markup=temp_keyboard)
    else:
        await message.reply("Имя не должно превышать 20 символов")
        await state.set_state(Registration.first_name)


@registration_router.message(Registration.second_name)
async def register_last_name(message: Message, state: FSMContext):
    if ls_validator(message.text):
        await state.update_data(second_name=message.text)
        await state.set_state(Registration.position)
        await message.answer("Пожалуйста напишите вашу позицию", reply_markup=position_keyboard)
    else:
        await message.reply("Фамилия не должно превышать 20 символов")
        await state.set_state(Registration.first_name)


@registration_router.message(Registration.position)
async def register_position(message: Message, state: FSMContext):
    if message.text in position_texts:
        await state.update_data(position=message.text)
        await state.set_state(Registration.degree)
        if message.text == "Преподователь" or message.text == 'Менеджер':
            await state.set_state(Registration.number)
            await message.reply("Пожалуйста отправьте ваш телефон номер", reply_markup=get_number)
        else:
            await message.answer('Выберите вашу степень.', reply_markup=degree_keyboard)
    else:
        await state.set_state(Registration.position)
        await message.answer('Выберите вашу позицию.', reply_markup=position_keyboard)


@registration_router.message(Registration.degree)
async def register_degree(message: Message, state: FSMContext):
    if message.text in degree_texts:
        await state.update_data(degree=message.text)
        await state.set_state(Registration.course)
        await message.answer('Введите ваш курс.')
    else:
        await state.set_state(Registration.position)
        await message.answer('Выберите вашу степень.', reply_markup=degree_keyboard)


@registration_router.message(Registration.course)
async def register_course(message: Message, state: FSMContext):
    data = await state.get_data()
    temp_range = range(1, 5) if data['degree'] == 'Бакалавр' else range(1, 2)
    if message.text.isdigit():
        if int(message.text) not in temp_range:
            await state.set_state(Registration.course)
            await message.answer('Введите ваш курс.')
        else:
            await state.update_data(course=int(message.text))
            await state.set_state(Registration.major)
            plaintext = ""
            majors = get_all_major()
            for major in majors:
                plaintext += f"{major.id}. {major.name}\n"
            await message.answer(f'Введите номер вашей специальности по следующему списку.\n'
                                 f'{plaintext}')
    else:
        await state.set_state(Registration.course)
        await message.answer('Введите ваш курс.')


@registration_router.message(Registration.major)
async def register_major(message: Message, state: FSMContext):
    plaintext = ""
    majors = get_all_major()
    ids = []
    for major in majors:
        plaintext += f"{major.id}. {major.name}\n"
        ids.append(major.id)
    if message.text.isdigit() and int(message.text) in ids:
        await state.update_data(major=int(message.text))
        await state.set_state(Registration.number)
        await message.reply("Пожалуйста отправьте ваш телефон номер", reply_markup=get_number)
    else:
        await state.set_state(Registration.major)
        await message.answer(f'Введите номер вашей специальности по следующему списку.\n'
                             f'{plaintext}')


@registration_router.message(Registration.number, F.contact)
async def register_number(message: Message, state: FSMContext):
    await state.update_data(number=message.contact.phone_number)
    user_data = await state.get_data()
    add_user_information(message.from_user.id, user_data)
    await message.answer("Вы успешно зарегистрировались!", reply_markup=main_keyboard)
    await state.clear()
