import operator

from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import (
    Row,
    ScrollingGroup,
    Select,
)


def type_transaction(on_click):
    return Row(
        Select(
            Format("{item}"),
            items=["Списание", "Перевод", "Пополнение"],
            item_id_getter=lambda x: x,
            id="select_type",
            on_click=on_click,
        ),
    )


def accout(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[name]}"),
            items="account",
            item_id_getter=operator.itemgetter("id"),
            id="select_accout",
            on_click=on_click,
        ),
        id="scrol_account",
        width=3,
        height=1,
    )


def category(on_click):
    return ScrollingGroup(
        Select(
            Format("{item[name]}"),
            items="category",
            item_id_getter=operator.itemgetter("id"),
            id="w_age",
            on_click=on_click,
        ),
        id="numbers",
        width=3,
        height=1,
    )
