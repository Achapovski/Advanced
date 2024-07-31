from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.widgets.kbd import Button, Row, Column, Group, Select, Checkbox, Multiselect, Radio
from aiogram_dialog.widgets.text import Const, Format, Multi, Case, List
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia, Media
from aiogram_dialog.widgets.input import TextInput, MessageInput
from environs import Env

from getters_and_funcs import *

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

router = Router()


class StartSG(StatesGroup):
    start = State()


start_dialog = Dialog(
    Window(
        List(field=Format('{item[0]}. {item[1]}'),
             items='items',
             page_size=2),
        getter=get_items,
        state=StartSG.start,
    ),
)

# Селектор
const_test_dialog = Dialog(
    Window(
        Case(
            texts={
                1: Format("Text number one {username}"),
                2: Format("Text number two {user_id}"),
                3: Const("Text number three"),
                ...: Const("Getter don`t return a number")
            },
            selector="number",
        ),
        getter=get_data,
        state=StartSG.start
    ),
)

# Список (item как объект цикла for, поэтому обращение через него происходит)
list_test_dialog = Dialog(
    Window(
        List(field=Format("<b>{item[0]}</b>. {item[1]}"),
             items="items",
             ),
        getter=get_random_list,
        state=StartSG.start,
    )
)


# Кнопки
button_test_dialog = Dialog(
    Window(
        Const(text="Inline buttons test"),
        Button(text=Const(text="Button"),
               id="button_id",
               on_click=on_click_func,
               when="1"),
        getter=get_true_or_false,
        state=StartSG.start
    )
)

# Столбцы и строки
button_row_column_dialog = Dialog(
    Window(
        Const(text="<b><code>Buttons</code></b>"),
        Column(
            Button(Const("Button 1"), id="b_1", on_click=on_click_func),
            Button(Const("Button 2"), id="b_2", on_click=on_click_func),
            Button(Const("Button 3"), id="b_3", on_click=on_click_func),
            when="1"
        ),
        getter=get_true_or_false,
        state=StartSG.start
    )
)

# Динамическое создание клавиатуры
select_dialog = Dialog(
    Window(
        Const("Select test widget"),
        Select(
            text=Format(text="{item[1]}"),
            items="categories",
            item_id_getter=lambda x: x[0],
            id="category",
            on_click=select,
        ),
        getter=getter_for_select,
        state=StartSG.start,
    ),
)

# Чек-бокс
check_box_dialog = Dialog(
    Window(
        Const(text="Default text"),
        Const("Additional text", when="checked"),
        Checkbox(
            checked_text=Const("Off"),
            unchecked_text=Const("On"),
            id="checkbox",
            default=False,
            on_state_changed=checkbox_click,
        ),
        getter=check_box_getter,
        state=StartSG.start
    )
)

# Множественный выбор
multiselect_dialog = Dialog(
    Window(
        Const(text="Отметьте темы новостей:"),
        Row(
            Multiselect(
                checked_text=Format("[✔️] {item[0]}"),
                unchecked_text=Format("[      ] {item[0]}"),
                id="multi_topics",
                item_id_getter=lambda x: x[1],
                items="topics",
                # Необязательные параметры: минимальное и максимальное количество выборов
                min_selected=1,
                max_selected=5,

                on_state_changed=multi_kbd_handler
                # Хэндлеры
                # on_state_changed=
                # on_click=
            ),
        ),
        Column(
            Button(
                text=Const("Confirm"),
                id="multi_kbd",
                on_click=multi_kbd_input_handler
            )
        ),
        getter=get_topics,
        state=StartSG.start,
    ),
)

# Выбор радио кнопок
radio_buttons_dialog = Dialog(
    Window(
        Format(text="{text}"),
        Radio(
            checked_text=Format('🔘 {item[0]}'),
            unchecked_text=Format('⚪️ {item[0]}'),
            id="radio_lang",
            item_id_getter=lambda x: x[1],
            items="languages",
        ),
        Button(
            text=Const("Confirm"),
            id="confirm_button",
            on_click=set_radio_answer
        ),
        getter=get_languages,
        state=StartSG.start,
    ),
    on_start=set_radio
)

static_dialog = Dialog(
    Window(
        Const(text="Just do it"),
        StaticMedia(
            # url=r"https:/...",
            path=Format("{picture}"),
            type=ContentType.PHOTO,
        ),
        Button(
            text=Const("Change pic"),
            id="button",

        ),
        getter=get_picture,
        state=StartSG.start
    )
)

text_dialog = Dialog(
    Window(
        Const(text="Введите ваш возраст"),
        TextInput(
            id="age_input",
            on_error=on_error,
            on_success=on_success,
            type_factory=age_check,
        ),
        MessageInput(
            func=any_message,
            content_types=ContentType.ANY,
        ),
        state=StartSG.start
    ),
)


@router.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
    # await dialog_manager.done()
    # await message.answer("Hi, Maxim")


dp.include_router(router)
dp.include_router(text_dialog)
setup_dialogs(dp)
dp.run_polling(bot)

# For test automation
