from aiogram_dialog import DialogManager


async def get_account(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    return {"account": ctx.start_data["account"]}  # type: ignore


async def get_category(dialog_manager: DialogManager, **kwargs):
    ctx = dialog_manager.current_context()
    res = []
    if ctx.dialog_data["type_transaction"] == "Списание":
        for item in ctx.start_data["category"]:  # type: ignore
            print(item)
            if item["typeName"] == "Debit":  # type: ignore
                res.append(item)
    else:
        for item in ctx.start_data["category"]:  # type: ignore
            if item["typeName"] == "Adding":  # type: ignore
                res.append(item)

    return {"category": res}  # type: ignore
