
from aiogram import types
import datetime as dt
# class Buttons:
#     confirmation_markup = types.ReplyKeyboardMarkup(
#         resize_keyboard=True,
#         one_time_keyboard=True
#     )

#     def confirm_number(self):
#         confirm_number = types.KeyboardButton(
#             text='Подтвердить номер телефона',
#             request_contact=True
#         )

#         self.confirmation_markup.add(confirm_number)

#         return self.confirmation_markup


#     def confirm_location(self):
#         confirm_location = types.KeyboardButton(
#             text='Подтвердить геолокацию',
#             request_location=True
#         )

#         self.confirmation_markup.add(confirm_location)

#         return self.confirmation_markup 


#     def main_menu(self):
#         menu_btn = types.KeyboardButton(
#             text='Меню 📖'
#         )

#         order_to_deliver_btn = types.KeyboardButton(
#             text='Заказать на вынос 🚗'
#         )

#         book_table_btn = types.KeyboardButton(
#             text='Забронировать столик 🍽'
#         )

#         feedback_btn = types.KeyboardButton(
#             text='Оставить отзыв 💭'
#         )


class Buttons:
    def main_buttons(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
            row_width=2
        )

        book_table_btn = types.KeyboardButton(
            text='Забронировать столик ⏰',
        )

        show_menu_btn = types.KeyboardButton(
            text='Перейти в меню 🗒',
        )

        set_feedback_btn = types.KeyboardButton(
            text='Отзывы ✅',
        )

        markup.add(
            book_table_btn,
            show_menu_btn,
            set_feedback_btn,
        )

        return markup


    def feedback_buttons(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )

        send_feedback_btn = types.KeyboardButton(
            text='Оставить отзыв ✍',
        )

        read_feedbacks_btn = types.KeyboardButton(
            text='Прочитать отзывы 👍',
        )


        markup.add(
            send_feedback_btn,
            read_feedbacks_btn,
        )

        return markup


    def back_to_menu(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )

        back_to_menu_btn = types.KeyboardButton(
            text='Назад в меню',
        )

        markup.add(back_to_menu_btn)

        return markup

    def confirm_phone_number(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )

        confirm_btn = types.KeyboardButton(
            text='Потвердить',
            request_contact=True
        )
         
        markup.add(confirm_btn)
        return markup

    def ask_phone(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        confirm_phone_btn = types.KeyboardButton(
            text='Потвердить номер телефона',
            request_contact=True
        )
        markup.add(confirm_phone_btn)
        return markup


    def ask_location(self):
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True,
            resize_keyboard=True,
        )
        confirm_location_btn = types.KeyboardButton(
            text ='Подтвердить геолокацию',
            request_location=True
        )

        markup.add(confirm_location_btn)
        return markup

class InlineButtons:
    def show_menu_buttons(self):
        markup = types.InlineKeyboardMarkup(
            row_width=2
        )
        
        primary_meal_btn = types.InlineKeyboardButton(
            text='Фирменные блюда',
            callback_data='primary_meal'
        )

        breakfast_btn = types.InlineKeyboardButton(
            text='Завтраки',
            callback_data='breakfast'
        )

        lunch_btn = types.InlineKeyboardButton(
            text='Обеды',
            callback_data='lunch'
        )

        dinner_btn = types.InlineKeyboardButton(
            text='Ужин',
            callback_data='dinner'
        )

        resto_site_btn = types.InlineKeyboardButton(
            text='Перейти на сайт',
            callback_data='resto',
            url='https://freehtml5.co/preview/?item=resto-free-responsive-bootstrap-4-template-for-restaurants'
        )

        markup.add(
            primary_meal_btn,
            breakfast_btn,
            lunch_btn,
            dinner_btn,
            resto_site_btn
        )

        return markup

    
    def make_order(self, definiton: tuple):
        """Функция которая создаёт inline-кнопку Заказать 🔥"""
        markup = types.InlineKeyboardMarkup(
            row_width=2
        )

        order_btn = types.InlineKeyboardButton(
            text='Заказать 🔥',
            callback_data=f'{definiton[0]} {definiton[1]}',
        )

        markup.add(order_btn)

        return markup

    def calendar(self):
        current_month = dt.datetime.today().month
        current_day = dt.datetime.today().day

        month = (
            'Январь',
            'Февраль',
            'Март',
            'Апрель',
            'Май',
            'Июнь',
            'Июль',
            'Август',
            'Сентябрь',
            'Октябрь',
            'Ноябрь',
            'Декабрь'
        )

        markup = types.InlineKeyboardMarkup(
            row_width=3
        )

        if current_month % 2 == 1:
            for i in range(current_day+1, 32):
                markup.add(
                    types.InlineKeyboardButton(
                    text = f'{month[current_month-1]} - {i}',
                    callback_data = f'{month[current_month-1]} {i}'
                    )
                )
            else:
                return markup 


        elif current_month % 2 == 0:
            if current_month == 2:
                limit = 29
            elif current_month == 8:
                limit = 32
            else:
                limit = 31

            for i in range(current_day+1, limit):
                markup.add(
                    types.InlineKeyboardButton(
                    text = f'{month[current_month-1]} - {i}',
                    callback_data = f'{month[current_month-1]} {i}'
                    )
                )
            else:
                return markup 
        
        
    def clock(self):
        time = (
            '09:00',
            '10:00',
            '11:00',
            '12:00',
            '13:00',
            '14:00',
            '15:00',
            '16:00',
            '17:00',
            '18:00',
            '19:00',
            '20:00',
            '21:00',
            '22:00',
            '23:00',
            '00:00',
        )

        markup = types.InlineKeyboardMarkup(
            row_width=3
        )

        for t in time:
            markup.add(
                types.InlineKeyboardButton(
                    text = f'{t} часов',
                    callback_data=t
                )
            )
        else:
            return markup