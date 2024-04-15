from aiogram_dialog.widgets.text import Format
from aiogram_dialog.widgets.kbd import Row, Select


def type_name_category(on_click):
    return Row(
        Select(
            Format("{item}"),
            items=["Списание", "Пополнение"],
            item_id_getter=lambda x: x,
            id="select_type",
            on_click=on_click,
        ),
    )
