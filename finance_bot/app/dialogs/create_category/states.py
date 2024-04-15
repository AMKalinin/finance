from aiogram.fsm.state import State, StatesGroup


class Category_create(StatesGroup):
    name = State()
    save = State()
