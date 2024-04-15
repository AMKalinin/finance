from aiogram.fsm.state import State, StatesGroup


class Category_create(StatesGroup):
    name = State()
    type_name = State()
    save = State()
