# -*- coding: utf-8 -*-
# It's a Telegram self.bot (telegram self.bot)
# Written by M1x7urk4
#
# █───█──█─██─██─████─█─█─████─█──█─█───
# ██─██─██──███──█──█─█─█─█──█─█─█──█──█
# █─█─█──█───█─────██─█─█─████─██───████
# █───█──█──███───██──█─█─█─█──█─█─────█
# █───█──█─██─██─██───███─█─█──█──█────█


# ---------------------------------------------------------------------------------------------------------------------
# Import libraries

from telebot import TeleBot
from config import BOT_TOKEN
import keyboard

from database import Database
from funcitons import get_user, print_error, log

import json


# ---------------------------------------------------------------------------------------------------------------------
# Different things for self.bot

# Creating database
db = Database()


# ---------------------------------------------------------------------------------------------------------------------
# Another classes

class User:
    def __init__(self, id, role=None, status='Пользователь', about=''):
        self.id = id
        self.role = role
        self.status = status
        self.beer_amount = 0
        self.about = about
        self.photo = None
        self.info = {
            'code_registered': None,
        }


class Role:
    def __init__(self, id, name='', duties=list()):
        self.id = id
        self.name = name
        self.duties = duties


class Access_code:
    def __init__(self, id, role='', code='', one_time=True):
        self.id = id
        self.role = role
        self.code = code
        self.one_time = one_time


class Duty:
    def __init__(self, id, name, about='', question=''):
        self.id = id
        self.name = name
        self.about = about
        self.question = question
        self.asnwers = list()

 
class Message:
    def __init__(self, id, user_id, time, answer='', text='', file=None):
        self.id = id
        self.user_id = user_id
        self.time = time
        self.answer = answer
        self.text = text
        self.file = file



# ---------------------------------------------------------------------------------------------------------------------
# The processing of incoming messages and commands

class Bot:
    def __init__(self):
        self.bot = TeleBot(token=BOT_TOKEN, threaded=True)
        self.users = list() # List of all users
    

    # Get user by id 
    def get_user(self, id):
        for user in self.users:
            if str(user.id) == str(id):
                return user
        return None
    
    
    # Get code by 'code'
    def get_code(self, code):
        for access_code in self.access_codes:
            if access_code.code == code:
                return access_code
        return None
    

    def run(self):
        
        # -------------------------------------------------------------------------------
        # The processing of incoming messages and commands

        # Start command
        @self.bot.message_handler(commands=['start'])
        def start_msg(message):
            try:
                if message.chat.type not in ('group', 'supergroup', 'channel'):

                    # if user is not exists
                    if not db.if_user_exists(message.from_user.id):
                        info = get_user(message)
                        new_user = (message.from_user.id, json.dumps(info))
                        db.users_add(new_user)
            
                        cur_user = User(id=message.chat.id)
                        self.users.append(cur_user)
                    else:
                        cur_user = self.get_user(message.chat.id)

                    if not cur_user.info['code_registered']:
                        # if user not registered (no code)
                        self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                            reply_markup=keyboard.menu())
                    else:
                        # if user registered (yes code)
                        self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                            reply_markup=keyboard.menu_reg())

            # Error
            except Exception as e:
                self.bot.send_message(message.from_user.id, 'Возникла ошибка')
                print_error(e)
        

        # -------------------------------------------------------------------------------
        # The processing of incoming text messages
        @self.bot.message_handler(content_types=['text', 'photo', 'document', 'video', 'contact', 'location'])
        def text_message(message):
            try:
                cur_user = self.get_user(message.chat.id)
                
                # if user is not exists
                if cur_user is None:
                    cur_user = User(id=message.chat.id)
                    self.users.append(cur_user)

                if not cur_user.info['code_registered']:
                    # if user not registered (no code)
                    if message.text == 'Ввести код':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                              text='Введите код:',
                                              reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, enter_code)
                    elif message.text == 'Связаться с админом':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                              text='Введите свой вопрос админу:',
                                              reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, enter_question)
                    elif message.text == 'Посмотреть информацию о компании':
                        pass
                else:
                    # if user registered (yes code)
                    pass

            # Error
            except Exception as e:
                self.bot.send_message(message.from_user.id, 'Возникла ошибка')
                print_error(e)

        
        # ---------------------------------------------------------------------------------------------------------------------
        # Next-step handlers

        def enter_code(message):
            cur_user = self.get_user(message.chat.id)

            if message.text == '<< Назад':
                if not cur_user.info['code_registered']:
                    # if user not registered (no code)
                    self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                        reply_markup=keyboard.menu())
                else:
                    # if user registered (yes code)
                    self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                        reply_markup=keyboard.menu_reg())
            else:
                db_code = db.access_codes_get_by_code(message.text)
                if db_code is not None:
                    code = Access_code(id=db_code[0], role=db_code[1], code=db_code[2], one_time=db_code[3])
                    
                    db_role = db.roles_get_one(code.role)
                    role = Role(id=db_role[0], name=db_role[1], duties=db_role[2])
                else:
                    code = None

                if code is None:
                    # Incorrect code
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                          text='Неправильный код!',
                                          reply_markup=keyboard.back())
                    self.bot.register_next_step_handler(msg, enter_code)
                else:
                    # Correct code
                    cur_user.info['code_registered'] = True
                    cur_user.role = role
                    
                    self.bot.send_message(chat_id=message.chat.id,
                                          text=f'Код успешно подтвержден!\nВам выдана роль: {cur_user.role.name}',
                                          reply_markup=keyboard.menu_reg())
        

        def enter_question(message):
            cur_user = self.get_user(message.chat.id)

            if message.text == '<< Назад':
                if not cur_user.info['code_registered']:
                    # if user not registered (no code)
                    self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                        reply_markup=keyboard.menu())
                else:
                    # if user registered (yes code)
                    self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺',
                                        reply_markup=keyboard.menu_reg())
            else:
                pass

        # ---------------------------------------------------------------------------------------------------------------------
        # Inline buttons

        # Some functions for processing of incoming text messages
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            try:
                text = call.data.split()
                print(text)

            except Exception as e:
                print_error(e)
                self.bot.send_message(call.from_user.id, 'Возникла ошибка')

        # ---------------------------------------------------------------------------------------------------------------------
        # Launch bot thread
        log(f'Бот запущен!')
        self.bot.infinity_polling()


# ---------------------------------------------------------------------------------------------------------------------
# Main loop

if __name__ == "__main__":
    bot = Bot()
    bot.run()
    