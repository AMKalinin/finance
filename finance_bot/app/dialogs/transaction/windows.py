from aiogram.enums import ContentType

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Calendar, Cancel, Row

from . import keyboards
from . import states
from . import getters
from . import selected


def type_transaction_window():
    return Window(
        Const("Выберите тип транзакции"),
        keyboards.type_transaction(selected.on_selected),
        Cancel(Const("Cancel")),
        state=states.Dialog_transaction.select_type,
    )


def account_from_window():
    return Window(
        Const("Выберите счет откуда взяты средства"),
        keyboards.accout(selected.on_selected),
        Cancel(Const("Cancel")),
        state=states.Dialog_transaction.from_state,
        getter=getters.get_account,
    )


def account_to_window():
    return Window(
        Const("Выберите счет куда будут отправлены средства"),
        keyboards.accout(selected.on_selected),
        Cancel(Const("Cancel")),
        state=states.Dialog_transaction.to_state,
        getter=getters.get_account,
    )


def select_categoty_window():
    return Window(
        Const("Выберите категорию"),
        keyboards.category(selected.on_selected),
        Cancel(Const("Cancel")),
        state=states.Dialog_transaction.category_state,
        getter=getters.get_category,
    )


def size_window():
    return Window(
        Const("Введите сумму"),
        Cancel(Const("Cancel")),
        MessageInput(content_types=[ContentType.TEXT], func=selected.on_input_size),
        state=states.Dialog_transaction.size,
    )


def description_window():
    return Window(
        Const("Ведите описание"),
        Cancel(Const("Cancel")),
        MessageInput(
            content_types=[ContentType.TEXT], func=selected.on_input_description
        ),
        state=states.Dialog_transaction.description,
    )


def select_date_window():
    return Window(
        Const("Выберите дату"),
        Calendar(id="calendar", on_click=selected.on_date_selected),
        state=states.Dialog_transaction.date,
    )


def save_window():
    return Window(
        Const("Сохранить транзакцию:"),
        Format("FROM: {dialog_data[FROM]}"),
        Format("TO: {dialog_data[TO]}"),
        Format("Category: {dialog_data[category]}"),
        Format("Size: {dialog_data[size]}"),
        Format("Description: {dialog_data[description]}"),
        Row(
            Button(Const("Да"), id="button", on_click=selected.on_save),
            Cancel(Const("Нет")),
        ),
        state=states.Dialog_transaction.save,
    )
