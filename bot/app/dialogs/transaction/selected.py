from datetime import date
from typing import Any
import aiohttp

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from .states import Dialog_transaction
from config import BASE_URL


async def on_selected(
    callback: CallbackQuery, widget: Any, manager: DialogManager, input_info: str
):
    ctx = manager.current_context()
    if not ctx.dialog_data:
        ctx.dialog_data.update(
            {
                "FROM": None,
                "TO": None,
                "category": None,
                "type_transaction": input_info,
                "step": 1,
            }
        )
        if input_info == "Списание":
            await manager.switch_to(Dialog_transaction.from_state)
        elif input_info == "Пополнение":
            await manager.switch_to(Dialog_transaction.category_state)
        elif input_info == "Перевод":
            await manager.switch_to(Dialog_transaction.from_state)

    elif ctx.dialog_data["step"] == 1:
        ctx.dialog_data["step"] = 2

        if ctx.dialog_data["type_transaction"] == "Списание":
            ctx.dialog_data["FROM"] = input_info
            await manager.switch_to(Dialog_transaction.category_state)

        elif ctx.dialog_data["type_transaction"] == "Пополнение":
            ctx.dialog_data["category"] = input_info
            await manager.switch_to(Dialog_transaction.to_state)

        elif ctx.dialog_data["type_transaction"] == "Перевод":
            ctx.dialog_data["FROM"] = input_info
            await manager.switch_to(Dialog_transaction.to_state)

    elif ctx.dialog_data["step"] == 2:
        if ctx.dialog_data["type_transaction"] == "Списание":
            ctx.dialog_data["category"] = input_info

        elif ctx.dialog_data["type_transaction"] == "Пополнение":
            ctx.dialog_data["TO"] = input_info

        elif ctx.dialog_data["type_transaction"] == "Перевод":
            ctx.dialog_data["TO"] = input_info

        await manager.switch_to(Dialog_transaction.size)


async def on_input_size(message: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    try:
        size = float(message.text)  # type: ignore
        ctx.dialog_data.update({"size": size})
        await manager.next()
    except ValueError:
        await manager.switch_to(Dialog_transaction.size)


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
