from typing import Any
from datetime import date

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import ChatEvent, Dialog, DialogManager, Window
from aiogram.enums import ContentType
from aiogram_dialog.widgets.kbd import (
    Button,
    Row,
    Select,
    ScrollingGroup,
    Cancel,
    Calendar,
)
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const, Format


class Dialog_transaction(StatesGroup):
    select_type = State()
    from_state = State()
    to_state = State()
    category_state = State()
    size = State()
    description = State()
    date = State()


async def to_FROM(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Dialog_transaction.from_state)


async def to_TO(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Dialog_transaction.to_state)


async def to_category(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Dialog_transaction.category_state)


async def selected(
    callback: CallbackQuery, widget: Any, manager: DialogManager, type_transaction: str
):
    ctx = manager.current_context()
    if not ctx.dialog_data:
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
        type_trans = ctx.dialog_data["type_transaction"]
        match type_trans:
            case "Списание":
                await manager.switch_to(Dialog_transaction.category_state)
            case "Пополнение":
                await manager.switch_to(Dialog_transaction.to_state)
            case "Перевод":
                await manager.switch_to(Dialog_transaction.to_state)
    elif ctx.dialog_data["step"] == 2:
        await manager.switch_to(Dialog_transaction.size)


async def go_back(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.back()


async def go_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.next()


async def on_input_size(message: Message, widget: MessageInput, manager: DialogManager):
    await message.answer("size - 599")
    await manager.next()


async def on_input_description(
    message: Message, widget: MessageInput, manager: DialogManager
):
    await message.answer("desc - asddsa")
    await manager.next()


async def on_date_selected(
    event: ChatEvent, widget: Any, dialog_manager: DialogManager, date: date
):
    await dialog_manager.done()


async def on_description(
    message: Message, widget: MessageInput, manager: DialogManager
):
    await message.answer("ssdjfsdf")
    await manager.next()


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
)
