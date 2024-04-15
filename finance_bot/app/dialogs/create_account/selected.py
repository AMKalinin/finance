import aiohttp

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button

from config import BASE_URL


async def on_input_name(message: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.update({"name": str(message.text)})
    await manager.next()


async def on_input_size(message: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    try:
        balance = float(message.text)  # type: ignore
        ctx.dialog_data.update({"balance": balance})
        await manager.next()
    except ValueError:
        await manager.next()


async def on_input_description(
    message: Message, widget: MessageInput, manager: DialogManager
):
    ctx = manager.current_context()
    ctx.dialog_data.update({"description": str(message.text)})
    await manager.next()


async def on_save(callback: CallbackQuery, button: Button, manager: DialogManager):
    ctx = manager.current_context()

    async with aiohttp.ClientSession() as session:
        async with session.post(BASE_URL + "/account/create", json=ctx.dialog_data):
            pass
    await manager.done()
