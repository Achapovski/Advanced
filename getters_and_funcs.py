import random

from aiogram.fsm.context import FSMContext
from aiogram_dialog.widgets.kbd import Button, ManagedCheckbox, ManagedMultiselect, ManagedRadio
from aiogram_dialog.manager.manager import DialogManager
from aiogram.types import User, CallbackQuery


async def get_data(event_from_user: User, **kwargs):
    number = random.randint(1, 100)
    return {
        "username": event_from_user.username or event_from_user.first_name,
        "user_id": event_from_user.id,
        "number": number,
    }


async def get_items(**kwargs):
    return {'items': (
        (1, 'Пункт 1'),
        (2, 'Пункт 2'),
        (3, 'Пункт 3'),
    )}


async def get_random_list(**kwargs):
    return {
        "items": ((1, "Text 1"),
                  (2, "Text 2"),
                  (3, "Text 3"),)
    }


async def get_true_or_false(**kwargs):
    return {"0": False, "1": True}


async def on_click_func(callback: CallbackQuery, button: Button, manager: DialogManager):
    # print(callback.data)
    # print(callback.model_dump_json(indent=4))
    print(manager.dialog_data)
    await callback.message.answer("Hello")


async def getter_for_select(**kwargs):
    categories = [
        (1, "car"),
        (2, "bike"),
        (3, "aircraft"),
        (4, "Avengers jet"),
    ]
    return {"categories": categories}


async def select(callback: CallbackQuery, button: Button, manager: DialogManager, item_id: str):
    print(callback.data)
    await callback.message.answer(callback.message.text)


async def checkbox_click(callback: CallbackQuery,
                         checkbox: ManagedCheckbox,
                         dialog_manager: DialogManager,
                         **kwargs):
    # print("handler", dialog_manager.dialog_data)
    print(callback.data)
    dialog_manager.dialog_data.update(checked=checkbox.is_checked())
    # return {"checked": checked}


async def check_box_getter(dialog_manager: DialogManager, **kwargs):
    checked = dialog_manager.dialog_data.setdefault("checked", False)
    # print("getter", dialog_manager.dialog_data)
    return {"checked": checked}


# Получение текстов для клавиатуры мультивыбора
async def get_topics(**kwargs):
    return {
        "topics": [("IT", 1),
                   ("Дизайн", 2),
                   ("Наука", 3),
                   ("Общество", 4), ]
    }


# Хэндлер для мульти клавиатуры
async def multi_kbd_handler(callback: CallbackQuery,
                            button: Button,
                            dialog_manager: DialogManager,
                            arg,
                            **kwargs):
    if arg in dialog_manager.dialog_data:
        del dialog_manager.dialog_data[arg]
    else:
        dialog_manager.dialog_data[arg] = True
    # print(kwargs.keys())
    # print(dialog_manager.dialog_data)
    # print(button.text)
    # print(callback.data)
    # await callback.message.answer("Ok...")


# Вывод конфирма клавиатуры мультивыбора
async def multi_kbd_input_handler(callback: CallbackQuery,
                                  button: Button,
                                  dialog_manager: DialogManager,
                                  *args):
    # Получение колбеков напрямую
    items: ManagedMultiselect = dialog_manager.find("multi_topics")
    print(items.get_checked())

    for item in dialog_manager.dialog_data:
        await callback.message.answer(item)
    # await callback.message.answer()


# Геттер радио кнопок
async def get_languages(dialog_manager: DialogManager, **kwargs):
    print(dialog_manager.start_data)
    return {"text": "Radio Buttons", "languages": [(1, 1), (2, 2), (3, 3)]}


# Установка ответа по умолчанию
async def set_radio(_, dialog_manager: DialogManager):
    radio: ManagedRadio = dialog_manager.find("radio_lang")
    await radio.set_checked(item_id="2")


# Хэндлер кадио кнопок
async def set_radio_answer(callback: CallbackQuery,
                           button: Button,
                           dialog_manager: DialogManager,
                           **kwargs):
    pars: ManagedRadio = dialog_manager.find("radio_lang")
    print(pars.get_checked())


# Геттер для статики
async def get_picture(dialog_manager: DialogManager,
                      *args,
                      **kwargs):
    picture = dialog_manager.dialog_data.setdefault("pic", 0)
    print(picture)
    print(dialog_manager.dialog_data)
    dialog_manager.dialog_data["pic"] = not picture
    path = [r"Dog.jpg", "Cat.JPEG"][picture]
    return {"picture": path}


# ----- Геттеры и хэндлеры для тексового ввода -----
async def on_success(*args, **kwargs):
    print(args)
    print(kwargs)


async def on_error(*args, **kwargs):
    print(args)
    print(kwargs)


def age_check(text: str, *args, **kwargs):
    print(args, kwargs)
    if text.isdigit():
        return text
    raise ValueError


async def any_message(*args, **kwargs):
    print(args)
    print(kwargs)