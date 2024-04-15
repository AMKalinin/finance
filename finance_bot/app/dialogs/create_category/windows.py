from aiogram.enums import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row

from . import states
from . import selected
from . import keyboards


def name_window():
    return Window(
        Const("Название категории"),
        MessageInput(content_types=[ContentType.TEXT], func=selected.on_input_name),
        Cancel(Const("Cancel")),
        state=states.Category_create.name,
    )


def type_name_window():
    return Window(
        Const("Тип категории"),
        keyboards.type_name_category(selected.on_type_name),
        # MessageInput(content_types=[ContentType.TEXT], func=selected.on_input_name),
        Cancel(Const("Cancel")),
        state=states.Category_create.name,
    )


def save_window():
    return Window(
        Const("Сохранить счет:"),
        Row(
            Button(Const("Да"), id="button", on_click=selected.on_save),
            Cancel(Const("Нет")),
        ),
        state=states.Category_create.save,
    )
