from aiogram_dialog import Dialog

from . import windows


def transaction_dialogs():
    return Dialog(
        windows.type_transaction_window(),
        windows.account_from_window(),
        windows.account_to_window(),
        windows.select_categoty_window(),
        windows.size_window(),
        windows.description_window(),
        windows.select_date_window(),
        windows.save_window(),
    )
