from aiogram_dialog import DialogManager


async def get_account(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {"account": ctx.start_data["account"]}  # type: ignore


async def get_category(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {"category": ctx.start_data["category"]}  # type: ignore
