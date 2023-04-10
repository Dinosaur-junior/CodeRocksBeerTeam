# -*- coding: utf-8 -*-
# It's a Telegram bot (database)

# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|


# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import inspect
import io
import time
from datetime import datetime

import pandas as pd
import psycopg2

import config


# ---------------------------------------------------------------------------------------------------------------------
# some functions

# get users name
def get_name(user):
    username = ''
    if user['first_name'] is not None:
        username += user['first_name']
    if user['last_name'] is not None:
        username += f" {user['last_name']}"
    if user['username'] is not None:
        username += f' @{user["username"]}'
    if username == '':
        username = str(user['id'])
    return username


# ---------------------------------------------------------------------------------------------------------------------
# database class
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                                     database=config.DATABASE_INFO['database'],
                                     user=config.DATABASE_INFO['user'],
                                     password=config.DATABASE_INFO['password'],
                                     port=config.DATABASE_INFO['port'])
        self.cur = self.conn.cursor()

        # tables
        self.tables = {'users': '''CREATE TABLE IF NOT EXISTS users 
                                    (id             BIGINT PRIMARY KEY   NOT NULL,
                                    info            JSON                 NOT NULL); ''',

                       }

    # print error
    def print_error(self, error):
        error_time = datetime.now(tz=config.TZ).strftime("%H:%M")
        error_name = inspect.getframeinfo(inspect.currentframe().f_back).filename
        error_line = error.__traceback__.tb_lineno
        error_function = inspect.getframeinfo(inspect.currentframe().f_back).function
        text = f'{error_time} -- {error_name}, line {error_line}, in {error_function}() -- {error}'

        self.conn.close()
        self.conn = psycopg2.connect(host=config.DATABASE_INFO['host'],
                                     database=config.DATABASE_INFO['database'],
                                     user=config.DATABASE_INFO['user'],
                                     password=config.DATABASE_INFO['password'],
                                     port=config.DATABASE_INFO['port'])
        self.cur = self.conn.cursor()
        print(text)

    # write data
    def insert(self, text, data=()):
        try:
            self.cur.execute(text, data)
            self.conn.commit()
        except Exception as e:
            self.print_error(e)
            print(text, data)

    # rollback
    def rollback(self):
        self.insert('ROLLBACK;')

    # fetchall
    def get_all(self, text, data=()):
        result = []
        for i in range(10):
            try:
                self.cur.execute(text, data)
                result = self.cur.fetchall()
                break
            except Exception as e:
                self.print_error(e)
            time.sleep(0.1)
        return result

    # fetchone
    def get_one(self, text, data=()):
        result = None
        for i in range(10):
            try:
                self.cur.execute(text, data)
                result = self.cur.fetchone()
            except Exception as e:
                self.print_error(e)
            time.sleep(0.1)
        return result

    # edit info
    def edit_info(self, object_type, object_id, key, value):
        self.insert(f"UPDATE {object_type} SET {key}=%s WHERE id=%s;", (value, object_id))

    # --------------------------------------

    # setup
    def setup(self):
        print('---\nStarting to configure the database')

        for table in self.tables:
            self.insert(self.tables[table])
            print(f'{table=} created')

        print('Database configuration completed\n---')

    # drop all tables
    def drop_all(self):
        print('---\nStarting to drop the database')

        for table in self.tables:
            self.insert(f'DROP table {table}')
            print(f'{table=} dropped')

        print('Drop configuration completed\n---')

    # --------------------------------------
    # users

    # get all users
    def users_get_all(self):
        return self.get_all('SELECT * FROM users;')

    # get user by id
    def users_get_one(self, user_id):
        return self.get_one("SELECT * FROM users WHERE id=%s;", (int(user_id),))

    # get user by username
    def users_get_by_username(self, username):
        return self.get_one("""SELECT * FROM users WHERE info ->> %s = %s;""", ('username', username.replace("@", ''),))

    # search user by id/username
    def get_user(self, user):
        user_by_id = None
        try:
            user_by_id = self.users_get_one(int(user))
        except:
            pass
        user_by_username = self.users_get_by_username(user)
        if user_by_id is None and user_by_username is None:
            return None
        elif user_by_id is not None:
            return user_by_id
        else:
            return user_by_username

    # delete user
    def users_delete(self, user_id):
        self.insert("DELETE FROM users WHERE id=%s;", (int(user_id),))

    # add user
    def users_add(self, new_user):
        if self.users_get_one(new_user[0]) is None:
            self.insert("INSERT INTO users(id, info)  VALUES(%s, %s);", new_user)

    # edit users info
    def users_update_info(self, user_id, key, value):
        self.insert(f"UPDATE users SET {key}=%s WHERE id=%s;", (value, user_id))

    # check if user exists
    def if_user_exists(self, user_id):
        user = self.users_get_one(user_id)
        return True if user is not None else False

    # --------------------------------------------
    # EXCEL STATISTIC

    # users(customers/executors) excel statistic
    def users_statistic(self):
        all_users = self.users_get_all()
        all_users.sort(key=lambda x: x[0])
        users = {'ID': [], 'Имя и юзернейм': [], 'Баланс': [], 'Подписка': [], 'Рефералы': [], 'Телефон': []}

        for user in all_users:
            try:
                users['ID'].append(user[0])
                users['Имя и юзернейм'].append(get_name(user[-1]))
                users['Баланс'].append(round(user[1], 2))
                end = '---'
                if user[2] is not None and user[2] > datetime.now():
                    end = user[2] - datetime.now()
                    end = str(end)[:str(end).rfind(".")]
                users['Подписка'].append(end)
                users['Рефералы'].append(' ,'.join(user[4]) if len(user[4]) > 0 else '-')
                users['Телефон'].append('---')

            except Exception as e:
                self.print_error(e)

        data = pd.DataFrame(users)

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        data.to_excel(writer, sheet_name='База пользователей', index=False)

        for column in data:
            column_width = max(data[column].astype(str).map(len).max(), len(column)) + 2
            col_idx = data.columns.get_loc(column)
            writer.sheets['База пользователей'].set_column(col_idx, col_idx, column_width)

        writer.close()
        out.seek(0)
        out.name = "users.xlsx"
        return out


if __name__ == '__main__':
    database = Database()
    # database.drop_all()
    database.setup()
