# -*- coding: utf-8 -*-
# It's a Telegram bot (functions)

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
import os
import secrets
import string
import time
from datetime import datetime
from threading import Thread

from __init__ import bot, path


# ---------------------------------------------------------------------------------------------------------------------
# FUNCTIONS


# check if value is ok
def check_type(value, checks_type):
    if type(value) == checks_type:
        return True
    else:
        flag = False
        try:
            checks_type(value)
            flag = True
        except:
            pass
        return flag


def print_error(e):
    error_name = inspect.getframeinfo(inspect.currentframe().f_back).filename
    error_line = e.__traceback__.tb_lineno
    error_function = inspect.getframeinfo(inspect.currentframe().f_back).function
    text = f'{error_name}, line {error_line}, in {error_function}() -- {e}'
    log(text)


def log(text):
    log_time = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
    log_file = open(os.path.join(path, 'log.txt'), 'a', encoding='utf-8')
    print(f'{log_time} -- {text}')
    print(f'{log_time} -- {text}', file=log_file)
    log_file.close()


# get users username
def get_username(user):
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


# get users username
def get_username_user(user):
    username = ''
    if user['username'] is not None:
        username += f'@{user["username"]}'

    if username == '':
        if user['first_name'] is not None:
            username += user['first_name']
        if user['last_name'] is not None:
            username += f" {user['last_name']}"

    if username == '':
        username = str(user['id'])
    return username


# get users name
def get_username_name(user):
    username = ''

    if user['first_name'] is not None:
        username += user['first_name']
    if user['last_name'] is not None:
        username += f" {user['last_name']}"

    if username == '':
        if user['username'] is not None:
            username += f'@{user["username"]}'

    if username == '':
        username = str(user['id'])
    return username


# get users username with name
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


# get user in dict
def get_user(message):
    user = {'id': message.from_user.id, 'first_name': message.from_user.first_name,
            'last_name': message.from_user.last_name, 'username': message.from_user.username}
    return user


# we divide the list into several small ones
def func_chunks_generators(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i: i + n]


# unknown message
def unknown_message(message, keyboard=None):
    # start command
    if message.text == '/start':
        bot.clear_step_handler_by_chat_id(message.from_user.id)
        bot.send_message(message.from_user.id, 'Добро пожаловать')

    # unknown message
    else:
        bot.send_message(message.from_user.id, 'Неизвестная команда', reply_markup=keyboard)


# anti sleep class
class AntiSleep(Thread):
    def __init__(self, bot_app):
        Thread.__init__(self)
        self.work = 0
        self.bot = bot_app

    def run(self):
        self.work = 1
        while self.work == 1:
            time.sleep(30)
            self.bot.get_me()


# create random string
def create_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    alphabet = alphabet.replace('/', '').replace('\\', '')
    password = ''.join(secrets.choice(alphabet) for _ in range(20))
    return password
