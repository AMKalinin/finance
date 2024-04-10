from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.enums import ParseMode

import json
import jinja2

import aiohttp

from keyboards.keyboard_start import get_yes_no_kb
from config import BASE_URL


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!", reply_markup=get_yes_no_kb())


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
async def create_transaction(message: Message):
    await message.answer("Выберите тип транзакции", reply_markup=ReplyKeyboardRemove())