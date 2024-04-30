from aiogram.fsm.state import State, StatesGroup


class Registration(StatesGroup):
    first_name = State()
    second_name = State()
    position = State()
    degree = State()
    course = State()
    major = State()
    number = State()
