from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Column, Group, Select, Checkbox, Multiselect, Radio
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia, Media
from aiogram_dialog.widgets.input import TextInput, MessageInput
from environs import Env

from getters_and_handlers import *

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


class DialogState(StatesGroup):
    first = State()
    second = State()
    third = State()
    fourth = State()


move_dialog = Dialog(
    Window(
        Format(text="Hello {user_name} !!!", when="show_hello"),
        Button(
            text=Const(text="Next ➡️"),
            on_click=go_next,
            id="button",
        ),
        getter=get_vars,
        state=DialogState.first
    ),
    Window(
        Const(text="<b>Second window</b>"),
        Button(
            text=Const(text="Back ⬅️"),
            on_click=go_back,
            id="button_back",
        ),
        Button(
            text=Const(text="Next ➡️"),
            on_click=go_next,
            id="button_next"
        ),
        state=DialogState.second
    ),
    Window(
        Const(text="<i><b>Third window</b></i>"),
        Button(
            text=Const(text="Back ⬅️"),
            on_click=go_back,
            id="button_next"
        ),
        Button(
            text=Const(text="Next ➡️"),
            on_click=go_next,
            id="button_back",
        ),
        state=DialogState.third
    ),
    Window(
        Const(text="<code>Fourth window</code>"),
        Button(
            text=Const(text="Back ⬅️"),
            on_click=go_back,
            id="button_back"
        ),
        Button(
            text=Const(text="Go to start ⬅️⬅️"),
            on_click=go_to_user_choice,
            id="button_start"
        ),
        state=DialogState.fourth
    ),
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(
        state=DialogState.first,
        mode=StartMode.RESET_STACK,
        data={"default_value": "Value", "States": DialogState}
    )
    # await message.answer("Hello")


if __name__ == "__main__":
    dp.include_router(router)
    dp.include_router(move_dialog)
    setup_dialogs(dp)
    dp.run_polling(bot)

