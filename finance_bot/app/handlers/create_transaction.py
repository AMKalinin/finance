from datetime import date
from typing import Any

from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import (
    Button,
    Calendar,
    Cancel,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format


class Dialog_transaction(StatesGroup):
    select_type = State()
    from_state = State()
    to_state = State()
    category_state = State()
    size = State()
    description = State()
    date = State()
    save = State()


async def selected(
    callback: CallbackQuery, widget: Any, manager: DialogManager, type_transaction: str
):
    ctx = manager.current_context()
    if not ctx.dialog_data:
        ctx.dialog_data.update({"FROM": None, "TO": None, "category": None})
        ctx.dialog_data.update({"type_transaction": type_transaction})
        ctx.dialog_data.update({"step": 1})
        match type_transaction:
            case "Списание":
                await manager.switch_to(Dialog_transaction.from_state)
            case "Пополнение":
                await manager.switch_to(Dialog_transaction.category_state)
            case "Перевод":
                await manager.switch_to(Dialog_transaction.from_state)
    elif ctx.dialog_data["step"] == 1:
        ctx.dialog_data.update({"step": 2})
        match ctx.dialog_data["type_transaction"]:
            case "Списание":
                ctx.dialog_data.update({"FROM": type_transaction})
                await manager.switch_to(Dialog_transaction.category_state)
            case "Пополнение":
                ctx.dialog_data.update({"category": type_transaction})
                await manager.switch_to(Dialog_transaction.to_state)
            case "Перевод":
                ctx.dialog_data.update({"FROM": type_transaction})
                await manager.switch_to(Dialog_transaction.to_state)
    elif ctx.dialog_data["step"] == 2:
        match ctx.dialog_data["type_transaction"]:
            case "Списание":
                ctx.dialog_data.update({"category": type_transaction})
            case "Пополнение":
                ctx.dialog_data.update({"TO": type_transaction})
            case "Перевод":
                ctx.dialog_data.update({"TO": type_transaction})
        await manager.switch_to(Dialog_transaction.size)


async def on_input_size(message: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    size = message.text
    ctx.dialog_data.update({"size": int(size)})
    await manager.next()


async def on_input_description(
    message: Message, widget: MessageInput, manager: DialogManager
):
    ctx = manager.current_context()
    ctx.dialog_data.update({"description": str(message.text)})
    await manager.next()


async def on_date_selected(
    event: ChatEvent, widget: Any, dialog_manager: DialogManager, date: date
):
    ctx = dialog_manager.current_context()
    ctx.dialog_data.update({"date": str(date)})
    await dialog_manager.next()


dialog = Dialog(
    Window(
        Const("Выберите тип транзакции"),
        Row(
            Select(
                Format("{item}"),
                items=["Списание", "Перевод", "Пополнение"],
                item_id_getter=lambda x: x,
                id="select_type",
                on_click=selected,
            ),
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.select_type,
    ),
    Window(
        Const("Выберите счет откуда взяты средства"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                items=["acc1", "acc2"],
                item_id_getter=lambda x: x,
                id="w_age",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.from_state,
    ),
    Window(
        Const("Выберите счет куда будут отправлены средства"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                items=["acc1", "acc2"],
                item_id_getter=lambda x: x,
                id="w_age",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.to_state,
    ),
    Window(
        Const("Выберите категорию"),
        ScrollingGroup(
            Select(
                Format("{item}"),
                items=["cat1", "cat2"],
                item_id_getter=lambda x: x,
                id="w_age",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.category_state,
    ),
    Window(
        Const("Введите сумму"),
        Cancel(Const("Cancel")),
        MessageInput(content_types=[ContentType.TEXT], func=on_input_size),
        state=Dialog_transaction.size,
    ),
    Window(
        Const("Ведите описание"),
        Cancel(Const("Cancel")),
        MessageInput(content_types=[ContentType.TEXT], func=on_input_description),
        state=Dialog_transaction.description,
    ),
    Window(
        Const("Выберите дату"),
        Calendar(id="calendar", on_click=on_date_selected),
        state=Dialog_transaction.date,
    ),
    Window(
        Const("Сохранить транзакцию:"),
        Format("FROM: {dialog_data[FROM]}"),
        Format("TO: {dialog_data[TO]}"),
        Format("Category: {dialog_data[category]}"),
        Format("Size: {dialog_data[size]}"),
        Format("Description: {dialog_data[description]}"),
        Row(Button(Const("Да"), id="button"), Cancel(Const("Нет"))),
        state=Dialog_transaction.save,
    ),
)
