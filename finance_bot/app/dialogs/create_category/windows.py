from aiogram.enums import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Cancel, Row

from . import states
from . import selected


def name_window():
    return Window(
        Const("Название счета"),
        MessageInput(content_types=[ContentType.TEXT], func=selected.on_input_name),
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
