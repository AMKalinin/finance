from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command

from keyboards.keyboard_start import get_yes_no_kb


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Hello!", reply_markup=get_yes_no_kb())


@router.message(F.text.lower() == "текущий баланс")
async def view_balance(message: Message):
    await message.answer("Ваш текущий баланс 0 !", reply_markup=ReplyKeyboardRemove())


@router.message(F.text.lower() == "создать транзакцию")
async def create_transaction(message: Message):
    await message.answer("Выберите тип транзакции", reply_markup=ReplyKeyboardRemove())
