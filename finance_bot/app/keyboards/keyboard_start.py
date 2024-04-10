from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_yes_no_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Текущий баланс")
    kb.button(text="Создать транзакцию")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)