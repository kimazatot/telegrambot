import psycopg2


create_users = '''CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_telegram_id VARCHAR(20) NOT NULL,
    first_name VARCHAR(25) NOT NULL, 
    last_name VARCHAR(25) NOT NULL, 
    position VARCHAR(25) NOT NULL, 
    phone_number VARCHAR(20) NOT NULL, 
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);'''

import psycopg2


create_users = '''CREATE TABLE users(
    user_id SERIAL PRIMARY KEY,
    user_telegram_id VARCHAR(20) NOT NULL,
    first_name VARCHAR(25) NOT NULL, 
    last_name VARCHAR(25) NOT NULL, 
    position VARCHAR(25) NOT NULL, 
    phone_number VARCHAR(20) NOT NULL, 
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);'''


create_feedbacks = '''CREATE TABLE feedbacks(
    feedback_id SERIAL PRIMARY KEY, 
    author_id VARCHAR(15) NOT NULL,
    author_first_name VARCHAR(25) NOT NULL,
    author_last_name VARCHAR(25) NOT NULL,
    author_phone_number VARCHAR(20) NOT NULL,
    feedback_text VARCHAR(255) NOT NULL,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);'''


create_meal_types = '''CREATE TABLE meal_types(
    id SERIAL PRIMARY KEY, 
    category VARCHAR(30) NOT NULL,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);'''


create_meal = '''CREATE TABLE meal(
    meal_id SERIAL PRIMARY KEY, 
    name VARCHAR(30) NOT NULL,
    meal_type SMALLINT NOT NULL,
    image_path VARCHAR(255) NOT NULL,
    price INT NOT NULL,
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_meal
    FOREIGN KEY(meal_type)
    REFERENCES meal_types(id)
);'''


create_orders = '''CREATE TABLE orders(
    order_id SERIAL PRIMARY KEY, 
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    meal_name VARCHAR(30) NOT NULL,
    meal_type SMALLINT NOT NULL,
    phone_number VARCHAR(20),
    location VARCHAR(50),
    date_created TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP);'''

class PostgreSQL:
    def __init__(self, *args, **kwargs):
        super(PostgreSQL, self).__init__(*args, **kwargs)
        self.connection = psycopg2.connect(
            dbname="telegram",
            host="localhost",
            user="postgres",
            password="0709045683kgg",
            port=5432
        )

        self.cursor = self.connection.cursor()


    def select(self, keys: tuple, table: str, *args, **kwargs):
        fields = ', '.join(keys)
        
        if args:
            if not isinstance(args[0], dict):
                raise TypeError('Неправильно переданы условия!')

            conditions = ''

            for key, value in args[0].items():
                conditions += f'{key} = \'{value}\','
            else:
                conditions = conditions[:-1]

            select_cmd = f'SELECT {fields} FROM {table} WHERE {conditions};'

        else:
            select_cmd = f'SELECT {fields} FROM {table};'

        self.cursor.execute(select_cmd)
        return self.cursor.fetchall()



    def insert(self, keys: tuple, values: tuple, table: str, *args, **kwargs):
        if not isinstance(keys, tuple) or not isinstance(values, tuple):
            raise TypeError('Не правильно переданы ключи или значения!')

        fields = ', '.join(keys)
        field_values = '('

        for f_v in values:
            field_values += f'\'{f_v}\','
        else:
            field_values = field_values[:-1] + ')'

        insert_cmd = f'INSERT INTO {table}({fields}) VALUES{field_values};'

        self.cursor.execute(insert_cmd)
        return self.connection.commit()



    def delete(self, values: dict, table: str, *args, **kwargs):
        if not isinstance(values, dict):
            raise TypeError('Не правильно переданы значения для условия!')

        elif len(values) == 0:
            raise ValueError('VALUES не может быть пустым!')

        condition = ''

        for field, value in values.items():
            condition += f'{field} = {value}'

        if args:
            condition += f' {args[0]}'

        insert_cmd = f'DELETE FROM {table} WHERE {condition};'

        self.cursor.execute(insert_cmd)
        return self.connection.commit()

    def create_db(self):
        self.cursor.execute(create_users)
        self.cursor.execute(create_feedbacks)
        self.cursor.execute(create_meal_types)
        self.cursor.execute(create_meal)

        return self.connection.commit()

if __name__ == "__main__":
    psql = PostgreSQL()
    # psql.insert(
    #     (
    #         'author_id',
    #         'author_first_name',
    #         'author_last_name',
    #         'author_phone_number',
    #         'feedback_text',
    #     ),
    #     (
    #         '541989549',
    #         'Joomart',
    #         'Ulukbekov',
    #         '+996703717180',
    #         'Очень понравился ресторан спасибо большое',
    #     ),
    #     'feedbacks'
    # )
    # psql.cursor.execute(create_orders)
    # psql.connection.commit()
    # psql.create_db()
    # psql.insert(
    #     (
    #         'user_telegram_id',
    #         'first_name',
    #         'last_name',
    #         'position',
    #         'phone_number',
    #     ),
    #     (
    #         '906622093',
    #         'Kim',
    #         'Adinay',
    #         'Chef',
    #         '+996703019024',
    #     ),
    #     'users'
    # )
    # psql.insert(
    #     ('category',),
    #     ('Фирменые блюда',),
    #     'meal_types'
    # )
    # psql.insert(
    #     ('category',),
    #     ('Завтраки',),
    #     'meal_types'
    # )
    # psql.insert(
    #     ('category',),
    #     ('Обеды',),
    #     'meal_types'
    # )
    # psql.insert(
    #     ('category',),
    #     ('Ужины',),
    #     'meal_types'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Каша рисовая',
    #         '2',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/breakfasts/kasha_ris.jpeg',
    #         '80',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Гренки',
    #         '2',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/breakfasts/grenki.jpeg',
    #         '65',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Яйца с Беконом',
    #         '2',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/breakfasts/eggs_bekon.jpeg',
    #         '125',
    #     ),'meal'
    # )



    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Борщ',
    #         '3',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/lunches/borsh.jpeg',
    #         '90',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Лагман',
    #         '3',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/lunches/lagman.jpeg',
    #         '80',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Плов',
    #         '3',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/lunches/plov.jpeg',
    #         '150',
    #     ),'meal'
    # )




    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Цезарь',
    #         '4',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/dinners/cesar.jpeg',
    #         '130',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Стэйк',
    #         '2',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/dinners/steak.jpeg',
    #         '210',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Спагетти',
    #         '2',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/dinners/spagetti.jpeg',
    #         '140',
    #     ),'meal'
    # )



    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Курица по-мексикански',
    #         '1',
    #         '/home/adinai/Desktop/pyfiles/telegrambot//images/primary/mexican_chiken.jpeg',
    #         '300',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Курица по_индийски',
    #         '1',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/primary/indian_chiken.webp',
    #         '270',
    #     ),'meal'
    # )

    # psql.insert(
    #     (
    #         'name',
    #         'meal_type',
    #         'image_path',
    #         'price',
    #     ),
    #     (
    #         'Сосиски с картошкой',
    #         '1',
    #         '/home/adinai/Desktop/pyfiles/telegrambot/images/primary/sasuge_potato.jpeg',
    #         '460',
    #     ),'meal'
    # )

    print(psql.select('*', 'meal'))

    psql.connection.close()