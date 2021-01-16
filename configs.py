from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from PIL import Image
import os
from aiogram.dispatcher.filters.state import State, StatesGroup

BOT_TOKEN = os.environ.get('BOT_TOKEN')


bot = Bot(BOT_TOKEN)
memory = MemoryStorage()
dispatcher = Dispatcher(bot=bot, storage=memory)



class BotStates(StatesGroup):
    """В этом классе просто хранятся переменные разных состояний.
        Если вызвать из класса переменную, то будет установленно состояние этой переменной."""
    show_main_menu_buttons = State()

    back_to_menu = State()
    
    list_meal = State()

    feedback_menu = State()
    get_feedback = State()

    confirm_number = State()
    user_confirmation = State()

    ask_phone = State()
    ask_location = State()

    check_inline_btns = State()
    check_clicked_button = State()

    set_day = State()
    set_time = State()
    booking_completed = State()


def resize_image(img_path):
    """Функция изменяет размер любой картинки на тот размер который Вы указали #image.resize(width, height)# """
    image = Image.open(img_path)
    new_image = image.resize((480, 512))
    new_image.save(img_path)
    return img_path