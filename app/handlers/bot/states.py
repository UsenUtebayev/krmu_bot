from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    working = State()
    end = State()
