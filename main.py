from ssl import MemoryBIO
from aiogram import executor, types
from aiogram.dispatcher.storage import FSMContext
from configs import dispatcher, bot, resize_image, BotStates
from buttons import InlineButtons, Buttons
from aiogram.types import Message, CallbackQuery, location, message
from datetime import date, datetime as dt
from db import PostgreSQL

btns = Buttons()
ibtns = InlineButtons()


@dispatcher.message_handler(commands=["start"], state='*')
async def welcome(message: Message):
    """Функция которая срабатывает при отправке боту команды /start."""
    welcome_sticker = open('/home/adinai/Desktop/lol.gif', 'rb')

    await bot.send_animation(
        chat_id=message.from_user.id,
        animation=welcome_sticker
    )

    await BotStates.show_main_menu_buttons.set()

    return await bot.send_message(
        chat_id=message.from_user.id,
        text=f'''
        *Здравствуйте, {message.from_user.first_name}*
        Компания Resto рада видеть Вас в нашем Телеграм боте!
        Вам будут доступны следующие функции:
        ''',
        parse_mode=types.ParseMode.MARKDOWN,
        reply_markup=btns.main_buttons()
    )



@dispatcher.message_handler(content_types=["text"], state=BotStates.show_main_menu_buttons)
async def main_response(message: Message):
    """После того как пользователь нажмёт на одну из кнопок, ему будет предложено соответствующее действие."""
    if message.text == 'Забронировать столик ⏰':
        await BotStates.set_day.set()
        return await bot.send_message(
            chat_id=message.from_user.id,
            text="Выберите день:",
            reply_markup=ibtns.calendar()
        )
    
    elif message.text == 'Перейти в меню 🗒':
        await BotStates.check_inline_btns.set()
        return await bot.send_message(
            chat_id=message.from_user.id,
            text="😋😋😋😋😋 Основное Меню 🍴 😋😋😋😋😋",
            reply_markup=ibtns.show_menu_buttons()
        )

    elif message.text == 'Отзывы ✅':
        await BotStates.feedback_menu.set()
        return await bot.send_message(
            chat_id=message.from_user.id,
            text="Выберите опцию:",
            reply_markup=btns.feedback_buttons()
        )
    elif message.text == 'Назад в меню':
        await BotStates.show_main_menu_buttons.set()

        return await bot.send_message(
            chat_id=message.from_user.id,
            text = 'Вам будут доступны следующие функции:',
            reply_markup = btns.main_buttons()
        )
    else:
        await BotStates.show_main_menu_buttons.set()

        return await bot.send_message(
            chat_id=message.from_user.id,
            text = 'Простите я вас не понял',
            reply_markup = btns.main_buttons()
        )

@dispatcher.callback_query_handler(state=BotStates.set_day)
async def booking_day(callback:CallbackQuery):
    if callback.data:
        global reservation_list
        reservation_list = []
        reservation_list.append(callback.data.split(' ')[0])
        reservation_list.append(callback.data.split(' ')[1])
        await BotStates.set_time.set()
    
        return await bot.send_message(
            chat_id = callback.from_user.id,
            text = 'выберите время:',
            reply_markup = ibtns.clock()

        )

@dispatcher.callback_query_handler(state=BotStates.set_time)
async def booking_time(callback:CallbackQuery):
    if callback.data:
        await BotStates.booking_completed.set()
        reservation_list.append(callback.data.split(' ')[0])
    
        return await bot.send_message(
            chat_id = callback.from_user.id,
            text = 'Потвердите номер телефона',
            reply_markup = btns.ask_phone()

        )

@dispatcher.message_handler(content_types=["contact"], state=BotStates.booking_completed)
async def confirm_number_for_reservation(message:Message):
    if message.contact is not None:

        psql = PostgreSQL()
        psql.insert(
            (
                'first_name',
                'last_name',
                'month_of_reservation',
                'day_of_reservation',
                'time_of_reservation',
                'phone_number',
            ),
            (
               message.from_user.first_name,
               message.from_user.last_name,
               reservation_list[0],
               reservation_list[1],
               reservation_list[2],
               message.contact.phone_number

            ),
            'reservations'
        )
        psql.connection.close()

        await BotStates.show_main_menu_buttons.set()

        return await bot.send_message(
            chat_id=message.from_user.id,
            text = '*Столик успешно забронирован 😅*',
            reply_markup=btns.main_buttons()
        )


@dispatcher.callback_query_handler(state=BotStates.check_inline_btns)
async def show_menu(callback: CallbackQuery):
    """Функция которая выводит список блюд по категориям.
        Всё зависит от нажатой inline-кнопки."""
    psql = PostgreSQL()
    await BotStates.user_confirmation.set()

    if callback.data == 'breakfast':
        for breakfast in psql.select(
            (
                'name', 'image_path', 'price', 'meal_type'
            ),
            'meal',
            {"meal_type": 2}
        ):
            image = resize_image(breakfast[1])
            await bot.send_photo(
                chat_id=callback.from_user.id,
                photo=open(image, 'rb'),
                caption=f'_Название:_ *{breakfast[0]}*\n_Цена:_ *{breakfast[2]} сом*',
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=ibtns.make_order((breakfast[-1], breakfast[0]))
            )
        else:
            return await bot.send_message(
                chat_id=callback.from_user.id,
                text='Нажмите "Назад" чтобы вернуться в Главное Меню!',
                reply_markup=btns.back_to_menu()
            )

    elif callback.data == 'lunch':
        for lunch in psql.select(
            (
                'name', 'image_path', 'price', 'meal_type'
            ),
            'meal',
            {"meal_type": 3}
        ):
            image = resize_image(lunch[1])
            await bot.send_photo(
                chat_id=callback.from_user.id,
                photo=open(image, 'rb'),
                caption=f'_Название:_ *{lunch[0]}*\n_Цена:_ *{lunch[2]} сом*',
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=ibtns.make_order((lunch[-1], lunch[0]))
            )
        else:
            return await bot.send_message(
                chat_id=callback.from_user.id,
                text='Нажмите "Назад" чтобы вернуться в Главное Меню!',
                reply_markup=btns.back_to_menu()
            )

    elif callback.data == 'dinner':
        for dinner in psql.select(
            (
                'name', 'image_path', 'price', 'meal_type'
            ),
            'meal',
            {"meal_type": 4}
        ):
            image = resize_image(dinner[1])
            await bot.send_photo(
                chat_id=callback.from_user.id,
                photo=open(image, 'rb'),
                caption=f'_Название:_ *{dinner[0]}*\n_Цена:_ *{dinner[2]} сом*',
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=ibtns.make_order((dinner[-1], dinner[0]))
            )
        else:
            return await bot.send_message(
                chat_id=callback.from_user.id,
                text='Нажмите "Назад" чтобы вернуться в Главное Меню!',
                reply_markup=btns.back_to_menu()
            )


    elif callback.data == 'primary_meal':
        for primary_meal in psql.select(
            (
                'name', 'image_path', 'price', 'meal_type'
            ),
            'meal',
            {"meal_type": 1}
        ):
            image = resize_image(primary_meal[1])
            await bot.send_photo(
                chat_id=callback.from_user.id,
                photo=open(image, 'rb'),
                caption=f'_Название:_ *{primary_meal[0]}*\n_Цена:_ *{primary_meal[2]} сом*',
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=ibtns.make_order((primary_meal[-1], primary_meal[0]))
            )
        else:
            return await bot.send_message(
                chat_id=callback.from_user.id,
                text='Нажмите "Назад в меню" чтобы вернуться в Главное Меню!',
                reply_markup=btns.back_to_menu()
            )
    



@dispatcher.callback_query_handler(state=BotStates.user_confirmation)
async def make_order(callback: CallbackQuery):
    global order_list
    order_list = []
    if callback.data:
        order_list.append(callback.data)

        await BotStates.ask_phone.set()

        return await bot.send_message(
            chat_id = callback.from_user.id,
            text = "Пожалуйуста подвердите свою личность",
            reply_markup=btns.ask_phone()
        )


@dispatcher.message_handler(content_types=["contact"], state=BotStates.ask_phone)
async def confirm_number_for_order(message:Message):
    if message.contact is not None:

        await BotStates.ask_location.set()
        order_list.append(message.contact.phone_number)

        return await bot.send_message(
            chat_id = message.from_user.id,
            text = 'Подвердите свою геолокация',
            reply_markup= btns.ask_location()
        )


@dispatcher.message_handler(content_types=["location"], state=BotStates.ask_location)
async def confirm_location_for_order(message: Message):
    if message.location is not None:
        psql = PostgreSQL()
        psql.insert(
            (
                'first_name',
                'last_name',
                'meal_name',
                'meal_type',
                'phone_number',
                'location',
            ),
            (
                message.from_user.first_name,
                message.from_user.last_name,
                order_list[0].split(' ')[1],
                order_list[0].split(' ')[0],
                order_list[1],
                f'{message.location.latitude} {message.location.longitude}'
            ),
            'orders'
        )
        await BotStates.check_clicked_button.set()

        psql.connection.close()

        return await bot.send_message(
            chat_id = message.from_user.id,
            text = 'Ваш заказ успешно сохранен'
        )


@dispatcher.message_handler(content_types=["text"], state=BotStates.feedback_menu)
async def feedbacks(message: Message):
    psql = PostgreSQL()
    if message.text == 'Оставить отзыв ✍':
        await BotStates.get_feedback.set()
        return await message.answer(
            text = '*Пожалуйста отправьте мне ваш отзыв!*',
            parse_mode = types.ParseMode.MARKDOWN
        )
    elif message.text == 'Прочитать отзывы 👍':
        feedbacks = psql.select(
            (
                'author_first_name',
                'author_last_name',
                'feedback_text',
                'date_created',
            ),
            'feedbacks'
        )
        for feedback in feedbacks:
            date_time = dt.strftime(feedback[-1], '%Y-%m-%d %H:%M')
            await bot.send_message(
                chat_id = message.from_user.id,
                text=f'*{feedback[0]} {feedback[1]}*\n\n{feedback[2]}\n\n_{date_time}_',
                parse_mode=types.ParseMode.MARKDOWN,
            )
        else:
            await BotStates.show_main_menu_buttons.set()
            await bot.send_message(
                chat_id = message.from_user.id,
                text='Для выхода в главное меню нажмите ⏩ *Назад в меню*',
                parse_mode=types.ParseMode.MARKDOWN,
                reply_markup=btns.back_to_menu()
            )
            psql.connection.close()
    else:
        await BotStates.feedback_menu.set()
        return await bot.send_message(
            chat_id=message.from_user.id,
            text="Выберите опцию:",
            reply_markup=btns.feedback_buttons()
        )

@dispatcher.message_handler(content_types=["text"], state=BotStates.get_feedback)
async def insert_feedback(message:Message):
    if message.text == '' or message.text == ' ':

        await BotStates.show_main_menu_buttons.set()

        return await bot.send_message(
            chat_id=message.from_user.id,
            text = '*Простите, Я Вас не понял 😅*',
            reply_markup = btns.main_buttons()
        )
    else:
        global feedback_message
        feedback_message = message
        await BotStates.confirm_number.set()
        return await message.answer(
            text='Подвердите номер телефона',
            reply_markup=btns.confirm_phone_number()
        )

@dispatcher.message_handler(content_types=["contact"], state=BotStates.confirm_number)
async def confirm_number_for_feedback(message:Message):
    if message.contact is not None:

        psql = PostgreSQL()
        psql.insert(
            (
                'author_id',
                'author_first_name',
                'author_last_name',
                'author_phone_number',
                'feedback_text',
            ),
            (
               feedback_message.from_user.id,
               feedback_message.from_user.first_name,
               feedback_message.from_user.last_name,
               message.contact.phone_number,
               feedback_message.text,
            ),
            'feedbacks'
        )
        psql.connection.close()

        await BotStates.feedback_menu.set()

        return await bot.send_message(
            chat_id=message.from_user.id,
            text = '*Ваш отзыв успешно сохранён 😅*',
            reply_markup=btns.feedback_buttons()
        )


if __name__ == '__main__':
    executor.start_polling(dispatcher=dispatcher)

# sudo apt-get install build-essential libssl-dev libffi-dev libxml2-dev libxslt1-dev python3.8-dev python3.9-dev