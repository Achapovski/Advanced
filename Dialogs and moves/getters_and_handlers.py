from aiogram.fsm.context import FSMContext
from aiogram_dialog.manager.manager import DialogManager
from aiogram.types import Message, CallbackQuery, ContentType, User
from aiogram_dialog.widgets.kbd import Button


async def get_vars(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {
        "user_name": event_from_user.first_name or event_from_user.username,
        "show_hello": True,
    }


async def go_next(callback: CallbackQuery,
                  button: Button,
                  dialog_manager: DialogManager,
                  **kwargs):
    await callback.answer("Ok, go next...")
    await dialog_manager.next()


async def go_back(callback: CallbackQuery,
                  button: Button,
                  dialog_manager: DialogManager,
                  **kwargs):
    await callback.answer("Ok, go back...")
    await dialog_manager.back()


async def go_to_user_choice(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager,
                            **kwargs):
    window_number = callback.data.find("button_start")
    await callback.answer(f"Ok, go to start")
    print(dialog_manager.start_data)
    await dialog_manager.switch_to(state=dialog_manager.start_data["States"].first)
    # await dialog_manager.switch_to(state=DialogState.first)
