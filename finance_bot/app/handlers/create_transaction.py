from datetime import date
from typing import Any
import aiohttp

from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
import operator
from aiogram_dialog.widgets.kbd import (
    Button,
    Calendar,
    Cancel,
    Row,
    ScrollingGroup,
    Select,
)
from aiogram_dialog.widgets.text import Const, Format

from config import BASE_URL


class Dialog_transaction(StatesGroup):
    select_type = State()
    from_state = State()
    to_state = State()
    category_state = State()
    size = State()
    description = State()
    date = State()
    save = State()


async def get_account(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {"account": ctx.start_data["account"]}  # type: ignore


async def get_category(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {"category": ctx.start_data["category"]}  # type: ignore


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
    ctx.dialog_data.update({"size": int(size)})  # type: ignore
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


async def on_save(callback: CallbackQuery, button: Button, manager: DialogManager):
    ctx = manager.current_context()
    dd = ctx.dialog_data
    match dd["type_transaction"]:
        case "Списание":
            type_operation = "Debit"
        case "Пополнение":
            type_operation = "Adding"
        case "Перевод":
            type_operation = "Transfer"

    data = {
        "FROM": dd["FROM"],
        "TO": dd["TO"],
        "size": float(dd["size"]),  # type: ignore
        "date": dd["date"],
        "category": dd["category"],
        "typeName": type_operation,
        "description": dd["description"],
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            BASE_URL + "/transaction/create", json=data
        ) as response:
            print(response)
    await manager.done()


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
                Format("{item[name]}"),
                items="account",
                item_id_getter=operator.itemgetter("id"),
                id="w_age",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.from_state,
        getter=get_account,
    ),
    Window(
        Const("Выберите счет куда будут отправлены средства"),
        ScrollingGroup(
            Select(
                Format("{item[name]}"),
                items="account",
                item_id_getter=operator.itemgetter("id"),
                id="select_to_acc",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.to_state,
        getter=get_account,
    ),
    Window(
        Const("Выберите категорию"),
        ScrollingGroup(
            Select(
                Format("{item[name]}"),
                items="category",
                item_id_getter=operator.itemgetter("id"),
                id="w_age",
                on_click=selected,
            ),
            id="numbers",
            width=3,
            height=1,
        ),
        Cancel(Const("Cancel")),
        state=Dialog_transaction.category_state,
        getter=get_category,
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
        Row(Button(Const("Да"), id="button", on_click=on_save), Cancel(Const("Нет"))),
        state=Dialog_transaction.save,
    ),
)
