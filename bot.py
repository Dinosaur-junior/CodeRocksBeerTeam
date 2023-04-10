# -*- coding: utf-8 -*-
# It's a Telegram bot (telegram bot)
# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|

# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import json

from __init__ import bot
from database import Database
from funcitons import get_user, print_error, AntiSleep, log

# ---------------------------------------------------------------------------------------------------------------------
# Different things for bot

# creating database
db = Database()


# ---------------------------------------------------------------------------------------------------------------------
# The processing of incoming messages and commands

# Start command
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        if message.chat.type not in ('group', 'supergroup', 'channel'):

            # if user is not exists
            if not db.if_user_exists(message.from_user.id):
                info = get_user(message)
                new_user = (message.from_user.id, json.dumps(info))
                db.users_add(new_user)

            bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺\n\n'
                                                   'Скоро здесь появится что-то интересное')

    # error
    except Exception as e:
        bot.send_message(message.from_user.id, 'Возникла ошибка')
        print_error(e)


# -------------------------------------------------------------------------------
# The processing of incoming text messages
@bot.message_handler(content_types=['text', 'photo', 'document', 'video', 'contact', 'location'])
def text_message(message):
    try:
        # if user is not exists
        if not db.if_user_exists(message.from_user.id):
            info = get_user(message)
            new_user = (message.from_user.id, json.dumps(info))
            db.users_add(new_user)

        bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺🍺🍺\n\n'
                                               'Скоро здесь появится что-то интересное')

    # error
    except Exception as e:
        bot.send_message(message.from_user.id, 'Возникла ошибка')
        print_error(e)


# ---------------------------------------------------------------------------------------------------------------------
# Inline buttons


# some functions for processing of incoming text messages
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    try:
        text = call.data.split()
        print(text)

    except Exception as e:
        print_error(e)
        bot.send_message(call.from_user.id, 'Возникла ошибка')


# ---------------------------------------------------------------------------------------------------------------------
# main loop

if __name__ == "__main__":
    # anti sleep
    anti_sleep_app = AntiSleep(bot)
    anti_sleep_app.start()

    log(f'Бот запущен: https://t.me/{bot.get_me().username}')
    # infinite bot launch
    while True:
        try:
            bot.polling()
        except Exception as error:
            print_error(error)
