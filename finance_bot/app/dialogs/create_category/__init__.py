from aiogram_dialog import Dialog

from . import windows


def category_create_dialogs():
    return Dialog(
        windows.name_window(), windows.type_name_window(), windows.save_window()
    )
