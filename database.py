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
                                    role            INT                           ,
                                    status          TEXT                 NOT NULL,
                                    beer_amount     BIGINT               NOT NULL,
                                    about           TEXT                         ,
                                    photo           BYTEA                        ,
                                    info            JSON                 NOT NULL); ''',

                       'roles': '''CREATE TABLE IF NOT EXISTS roles 
                                    (id             SERIAL PRIMARY KEY   NOT NULL,
                                    name            TEXT                 NOT NULL,
                                    duties          INT   ARRAY          NOT NULL); ''',

                       'access_codes': '''CREATE TABLE IF NOT EXISTS access_codes 
                                    (id             SERIAL PRIMARY KEY   NOT NULL,
                                    role            INT                  NOT NULL,
                                    code            TEXT                 NOT NULL,
                                    one_time        BOOLEAN              NOT NULL); ''',

                       'duties': '''CREATE TABLE IF NOT EXISTS duties 
                                    (id             SERIAL PRIMARY KEY   NOT NULL,
                                    name            TEXT                 NOT NULL,
                                    about           TEXT                 NOT NULL,
                                    question        TEXT                 NOT NULL,
                                    answers         JSON                 NOT NULL); ''',

                       'messages': '''CREATE TABLE IF NOT EXISTS messages
                                     (id              SERIAL PRIMARY KEY   NOT NULL,
                                     user_id          BIGINT               NOT NULL,
                                     time             TIMESTAMP            NOT NULL,
                                     answer           BOOLEAN              NOT NULL,
                                     text             TEXT                         ,
                                     file             BYTEA                        ); ''',

                       'jobs': '''CREATE TABLE IF NOT EXISTS jobs
                                    (id              SERIAL PRIMARY KEY   NOT NULL,
                                    name             TEXT                 NOT NULL,
                                    description      TEXT                 NOT NULL,
                                    photo            BYTEA                NOT NULL); ''',

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
            self.insert("INSERT INTO users(id, role, status, beer_amount, about, photo, info)  "
                        "VALUES(%s, %s, %s, %s, %s, %s, %s);", new_user)

    # edit users info
    def users_update_info(self, user_id, key, value):
        self.insert(f"UPDATE users SET {key}=%s WHERE id=%s;", (value, user_id))

    # check if user exists
    def if_user_exists(self, user_id):
        user = self.users_get_one(user_id)
        return True if user is not None else False

    # --------------------------------------
    # duties

    # get all duties
    def duties_get_all(self):
        return self.get_all('SELECT * FROM duties;')

    # get duties by id
    def duties_get_one(self, duties_id):
        return self.get_one("SELECT * FROM duties WHERE id=%s;", (int(duties_id),))

    # get duties by name
    def duties_get_by_name(self, duties_name):
        return self.get_one("""SELECT * FROM duties WHERE name=%s;""", (duties_name,))

    # delete duties
    def duties_delete(self, duties_id):
        self.insert("DELETE FROM duties WHERE id=%s;", (int(duties_id),))

    # add duties
    def duties_add(self, new_duties):
        self.insert("INSERT INTO duties(name, about, question, answers) VALUES(%s, %s, %s, %s);", new_duties)

    # edit duties info
    def duties_update_info(self, duties_id, key, value):
        self.insert(f"UPDATE duties SET {key}=%s WHERE id=%s;", (value, duties_id))

    # --------------------------------------
    # roles

    # get all roles
    def roles_get_all(self):
        return self.get_all('SELECT * FROM roles;')

    # get roles by id
    def roles_get_one(self, roles_id):
        return self.get_one("SELECT * FROM roles WHERE id=%s;", (int(roles_id),))

    # get roles by name
    def roles_get_by_name(self, role_name):
        return self.get_one("""SELECT * FROM roles WHERE name=%s;""", (role_name,))

    def roles_get_by_duty(self, duty_id):
        return self.get_all("""SELECT * FROM roles WHERE  WHERE %s=ANY(duties);""", (duty_id,))

    # delete roles
    def roles_delete(self, roles_id):
        self.insert("DELETE FROM roles WHERE id=%s;", (int(roles_id),))

    # add roles
    def roles_add(self, new_roles):
        self.insert("INSERT INTO roles(name, duties)  VALUES(%s, %s);", new_roles)

    # edit roles info
    def roles_update_info(self, roles_id, key, value):
        self.insert(f"UPDATE roles SET {key}=%s WHERE id=%s;", (value, roles_id))

    # --------------------------------------
    # access_codes

    # get all access_codes
    def access_codes_get_all(self):
        return self.get_all('SELECT * FROM access_codes;')

    # get access_codes by id
    def access_codes_get_one(self, access_codes_id):
        return self.get_one("SELECT * FROM access_codes WHERE id=%s;", (int(access_codes_id),))

    # get access_codes by code
    def access_codes_get_by_code(self, access_code):
        return self.get_one("""SELECT * FROM access_codes WHERE code=%s;""", (access_code,))

    def access_codes_get_by_role(self, duty_id):
        return self.get_all("""SELECT * FROM access_codes WHERE role=%s;""", (duty_id,))

    # delete access_codes
    def access_codes_delete(self, access_codes_id):
        self.insert("DELETE FROM access_codes WHERE id=%s;", (int(access_codes_id),))

    # add access_codes
    def access_codes_add(self, new_access_codes):
        self.insert("INSERT INTO access_codes(role, code, one_time) VALUES(%s, %s, %s);", new_access_codes)

    # --------------------------------------
    # messages

    # get all messages
    def messages_get_all(self):
        return self.get_all('SELECT * FROM messages;')

    def messages_get_all_by_user(self, user_id):
        return self.get_all('SELECT * FROM messages WHERE user_id=%s;', (user_id,))

    # get messages by id
    def messages_get_one(self, messages_id):
        return self.get_one("SELECT * FROM messages WHERE id=%s;", (int(messages_id),))

    # add messages
    def messages_add(self, new_messages):
        self.insert("INSERT INTO messages(user_id, time, answer, text, file)  "
                    "VALUES(%s, %s, %s, %s, %s);", new_messages)

    def unread_messages(self):
        return self.get_all("SELECT id FROM users WHERE info ->> 'unread' = 'True';")

    def users_get_with_dialogs(self):
        messages = self.messages_get_all()
        users_ids = list(set([i[1] for i in messages]))
        return [self.users_get_one(i) for i in users_ids]

    # --------------------------------------
    # jobs

    # get all jobs
    def jobs_get_all(self):
        return self.get_all('SELECT * FROM jobs;')

    # get jobs by id
    def jobs_get_one(self, jobs_id):
        return self.get_one("SELECT * FROM jobs WHERE id=%s;", (int(jobs_id),))

    # add jobs
    def jobs_add(self, new_jobs):
        self.insert("INSERT INTO jobs(name, description, photo) VALUES(%s, %s, %s);", new_jobs)

    # delete jobs by id
    def jobs_delete(self, jobs_id):
        return self.get_one("DELETE * FROM jobs WHERE id=%s;", (int(jobs_id),))

    # --------------------------------------------
    # EXCEL STATISTIC

    # users(customers/executors) excel statistic
    def users_statistic(self):
        all_users = self.users_get_all()
        all_users.sort(key=lambda x: x[0])
        users = {'ID': [], 'Имя и юзернейм': []}

        for user in all_users:
            try:
                users['ID'].append(user[0])
                users['Имя и юзернейм'].append(get_name(user[-1]))

            except Exception as e:
                self.print_error(e)

        data = pd.DataFrame(users)

        out = io.BytesIO()
        writer = pd.ExcelWriter(out, engine='xlsxwriter')
        data.to_excel(writer, sheet_name='База пользователей', index=False)

        for column in data:
            column_width = min(25, max(data[column].astype(str).map(len).max(), len(column)) + 2)
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
