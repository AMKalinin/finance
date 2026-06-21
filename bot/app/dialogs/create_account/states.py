from aiogram.fsm.state import State, StatesGroup


class Account_create(StatesGroup):
    name = State()
    size = State()
    description = State()
    save = State()
