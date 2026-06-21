from aiogram_dialog import Dialog

from . import windows


def account_create_dialogs():
    return Dialog(
        windows.name_window(),
        windows.size_window(),
        windows.description_window(),
        windows.save_window(),
    )
