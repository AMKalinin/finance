import json

import aiohttp
import jinja2
from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager
from config import BASE_URL
from keyboards.keyboard_start import get_main_kb

from .create_transaction import Dialog_transaction, dialog

router = Router()
router.include_router(dialog)


async def get_data(**kwargs):
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + "/account/") as response:
            account = await response.text()
            account = json.loads(account)
        async with session.get(BASE_URL + "/category/") as response:
            category = await response.text()
            category = json.loads(category)
    return {"account": account, "category": category}


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!", reply_markup=get_main_kb())


@router.message(F.text.lower() == "текущий баланс")
async def view_balance(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get(BASE_URL + "/account/") as response:

            body = await response.text()
            body = json.loads(body)  # TODO переделать через pydantic model
            total_balance = sum([x["balance"] for x in body])
            enviroment = jinja2.Environment(
                loader=jinja2.FileSystemLoader("app/templates/")
            )
            template = enviroment.get_template("balance.html")

            await message.answer(
                template.render(total_balance=total_balance, account_list=body),
                parse_mode=ParseMode.HTML,
            )


@router.message(F.text.lower() == "создать транзакцию")
async def create_transaction(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Dialog_transaction.select_type, data=await get_data())
