from aiogram.fsm.state import State, StatesGroup


class Dialog_transaction(StatesGroup):
    select_type = State()
    from_state = State()
    to_state = State()
    category_state = State()
    size = State()
    description = State()
    date = State()
    save = State()
