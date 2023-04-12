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

import json
import os
from datetime import datetime

from telebot import TeleBot

import keyboard
from config import BOT_TOKEN, path
from database import Database
from funcitons import get_user, print_error, log, get_name

# ---------------------------------------------------------------------------------------------------------------------
# Different things for self.bot

# Creating database
db = Database()

# Tmp user actions variables
user_actions = dict()


# ---------------------------------------------------------------------------------------------------------------------
# Another classes

class User:
    def __init__(self, id, role=None, status='Только что зарегистрировался', about=''):
        self.id = id
        self.role = role
        self.status = status
        self.beer_amount = 0
        self.about = about
        self.photo = None
        self.info = dict()


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
    def __init__(self, id, name, about='', question='', answers=dict()):
        self.id = id
        self.name = name
        self.about = about
        self.question = question
        self.answers = answers


class Message:
    def __init__(self, id, user_id, time, answer='', text='', file=None):
        self.id = id
        self.user_id = user_id
        self.time = time
        self.answer = answer
        self.text = text
        self.file = file


class Question:
    def __init__(self, id, question='', answer=''):
        self.id = id
        self.question = question
        self.answer = answer


# ---------------------------------------------------------------------------------------------------------------------
# The processing of incoming messages and commands

class Bot:
    def __init__(self):
        self.bot = TeleBot(token=BOT_TOKEN, threaded=True)
        self.users = list()  # List of all users : User
        self.duties = list()  # List of all duties : Duty

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

                    cur_user = self.get_user(message.chat.id)
                    if cur_user is None:
                        cur_user = User(id=message.chat.id)
                        self.users.append(cur_user)

                        # if user is not exists
                        if not db.if_user_exists(message.from_user.id):
                            info = get_user(message)
                            cur_user.info = info
                            new_user = (message.from_user.id,
                                        cur_user.role,
                                        cur_user.status,
                                        cur_user.beer_amount,
                                        cur_user.about,
                                        cur_user.photo,
                                        json.dumps(cur_user.info))
                            db.users_add(new_user)
                        else:
                            # if user exist - get from db
                            db_user = db.users_get_one(message.chat.id)
                            cur_user.role = db_user[1]
                            cur_user.status = db_user[2]
                            cur_user.beer_amount = db_user[3]
                            cur_user.about = db_user[4]
                            cur_user.photo = db_user[5]
                            cur_user.info = db_user[6]

                    if cur_user.role is None:
                        # if user not registered (no code)
                        self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺\n\n'
                                                                    'Запросите у админа код, чтобы получить доступ к боту',
                                              reply_markup=keyboard.menu())
                    else:
                        # if user registered (yes code)
                        self.bot.send_message(message.from_user.id, 'Добро пожаловать в нашу пивоварню! 🍺',
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
                if cur_user is None:
                    cur_user = User(id=message.chat.id)
                    self.users.append(cur_user)

                    # if user is not exists
                    if not db.if_user_exists(message.from_user.id):
                        info = get_user(message)
                        cur_user.info = info
                        new_user = (message.from_user.id,
                                    cur_user.role,
                                    cur_user.status,
                                    cur_user.beer_amount,
                                    cur_user.about,
                                    cur_user.photo,
                                    json.dumps(cur_user.info))
                        db.users_add(new_user)
                    else:
                        # if user exist - get from db
                        db_user = db.users_get_one(message.chat.id)
                        cur_user.role = db_user[1]
                        cur_user.status = db_user[2]
                        cur_user.beer_amount = db_user[3]
                        cur_user.about = db_user[4]
                        cur_user.photo = db_user[5]
                        cur_user.info = db_user[6]

                if cur_user.role is None:
                    # if user not registered (no code)
                    main_keyboard = keyboard.menu
                else:
                    # if user registered (yes code)
                    main_keyboard = keyboard.menu_reg

                if cur_user.role is None:
                    # if user not registered (no code)
                    if message.text == '🐈 Ввести код':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Введите код:',
                                                    reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, enter_code)
                    elif message.text == '📲 Связаться с админом':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Введите свой вопрос админу:',
                                                    reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, enter_question)
                    elif message.text == 'ℹ️ Посмотреть информацию о компании':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Предлагаю Вам пройти эксурс по компании в игровой форме, нажмите СТАРТ, если хотите начать',
                                                    reply_markup=keyboard.start_btn())
                        self.bot.register_next_step_handler(msg, start_cmp_info_game)
                    else:
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Неизвестная команда!',
                                                    reply_markup=main_keyboard())
                else:
                    # if user registered (yes code)
                    if message.text == '❓ Частые вопросы':
                        db_questions = db.questions_get_all()
                        questions = [Question(id=db_question[0],
                                              question=db_question[1],
                                              answer=db_question[2]) for db_question in db_questions]
                        self.bot.send_message(chat_id=message.chat.id,
                                              text=f'Частые вопросы пользователей:',
                                              reply_markup=keyboard.often_questions(questions))

                    elif message.text == '👨🏿‍💻 Мои коллеги':
                        db_users = db.users_get_all()
                        db_users = [i for i in db_users if i[1] is not None]
                        db_users.sort(key=lambda x: x[0])
                        if message.chat.id not in user_actions:
                            user_actions[message.chat.id] = {'nav_bar_id': 0}

                        while user_actions[message.chat.id]['nav_bar_id'] < len(db_users):
                            id = user_actions[message.chat.id]['nav_bar_id']
                            role = db.roles_get_one(db_users[id][1])[1]
                            if db_users[id][5] is not None:
                                self.bot.send_photo(chat_id=message.chat.id,
                                                    photo=db_users[id][5],
                                                    caption=f'Описание: {db_users[id][4] if  len(db_users[id][4]) > 0 else "тут пока пусто :("}\nДолжность: {role}\n{get_name(db_users[id][-1])}',
                                                    reply_markup=keyboard.nav_bar(
                                                        user_actions[message.chat.id]['nav_bar_id'], len(db_users)),
                                                    parse_mode='HTML')
                                break
                            else:
                                try:
                                    self.bot.send_message(chat_id=message.chat.id,
                                                          text=f'Описание: {db_users[id][4] if  len(db_users[id][4]) > 0 else "тут пока пусто :("}\nДолжность: {role}\n{get_name(db_users[id][-1])}',
                                                          reply_markup=keyboard.nav_bar(
                                                              user_actions[message.chat.id]['nav_bar_id'],
                                                              len(db_users)),
                                                          parse_mode='HTML')
                                    break
                                except:
                                    user_actions[message.chat.id]['nav_bar_id'] += 1
                                    if user_actions[message.chat.id]['nav_bar_id'] == len(db_users):
                                        user_actions.pop(message.chat.id)
                                        self.bot.send_message(chat_id=message.chat.id,
                                                              text='Пользователей не найдено!',
                                                              reply_markup=keyboard.menu_reg())
                                        break

                    elif message.text == '❗️ Мои обязанности':
                        if cur_user.info['training_done']:
                            duties = db.get_duties_by_role_id(cur_user.role)
                            duties = [i[1] for i in duties]
                            duties = '\n'.join(duties)
                            self.bot.send_message(chat_id=message.chat.id,
                                                  text=f'Ваши обязанности:\n{duties}')
                        else:
                            self.bot.send_message(chat_id=message.chat.id,
                                                  text='Для начала пройдите обучение, чтобы получить доступ к Вашми обязанностям!',
                                                  reply_markup=keyboard.menu_reg())

                    elif message.text == '📚 Пройти обучение':
                        if cur_user.info['training_done']:
                            msg = self.bot.send_message(chat_id=message.chat.id,
                                                        text='Вы уже прошли обучение.\nПройти снова?',
                                                        reply_markup=keyboard.training_again())
                            self.bot.register_next_step_handler(msg, training_again)
                        else:
                            db.users_update_info(message.chat.id, 'status', 'Обучение обязанностям - страница 1')
                            db_duties = db.get_duties_by_role_id(cur_user.role)

                            self.duties = [Duty(id=db_duty[0],
                                                name=db_duty[1],
                                                about=db_duty[2],
                                                question=db_duty[3],
                                                answers=db_duty[4]) for db_duty in db_duties]
                            self.bot.send_message(chat_id=message.chat.id,
                                                  text=f'Обязанность №1: {self.duties[0].name}\n\nОписание: {self.duties[0].about}\n\nВопрос: {self.duties[0].question}',
                                                  reply_markup=keyboard.duties_training(0, self.duties[0].answers))
                    elif message.text == '📲 Связаться с админом':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Введите свой вопрос админу:',
                                                    reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, enter_question)

                    elif message.text == 'ℹ️ Информация о компании':
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Предлагаю Вам пройти эксурс по компании в игровой форме, нажмите СТАРТ, если хотите начать',
                                                    reply_markup=keyboard.start_btn())
                        self.bot.register_next_step_handler(msg, start_cmp_info_game)

                    elif message.text == '🗺 Карта офиса':
                        self.bot.send_photo(chat_id=message.chat.id,
                                            photo=open(os.path.join(path, 'static', 'office_map.jpg'), 'rb'),
                                            caption='Не заблудитесь!')

                    elif message.text == '👤 Мой профиль':
                        cur_user = db.users_get_one(message.chat.id)
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text=f'Ваш профиль:\n\n'
                                                         f'Должность: {db.roles_get_one(cur_user[1])[1]}\n'
                                                         f'Кол-во пива: {cur_user[3]} шт.',
                                                    reply_markup=keyboard.profile())
                        self.bot.register_next_step_handler(msg, profile_main_page)

                    else:
                        msg = self.bot.send_message(chat_id=message.chat.id,
                                                    text='Неизвестная команда!',
                                                    reply_markup=main_keyboard())

            # Error
            except Exception as e:
                self.bot.send_message(message.from_user.id, 'Возникла ошибка')
                print_error(e)

        # ---------------------------------------------------------------------------------------------------------------------
        # Next-step handlers

        def enter_code(message):
            cur_user = self.get_user(message.chat.id)

            if message.text == '<< Назад':
                if cur_user.role is None:
                    # if user not registered (no code)
                    self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
                                          reply_markup=keyboard.menu())
                else:
                    # if user registered (yes code)
                    self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
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
                    cur_user.role = role

                    # update db
                    db.users_update_info(message.chat.id, "role", cur_user.role.id)

                    # if one-time code
                    if code.one_time:
                        db.access_codes_delete(code.id)

                    self.bot.send_message(chat_id=message.chat.id,
                                          text=f'Код успешно подтвержден!\nВам выдана роль: {cur_user.role.name}',
                                          reply_markup=keyboard.menu_reg())

        def enter_question(message):
            cur_user = self.get_user(message.chat.id)

            if cur_user.role is None:
                # if user not registered (no code)
                cur_keyboard = keyboard.menu
            else:
                # if user registered (yes code)
                cur_keyboard = keyboard.menu_reg

            if message.text == '<< Назад':
                self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
                                      reply_markup=cur_keyboard())
            elif message.content_type not in ['photo', 'text']:
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Вопрос может быть либо текстовый, либо картинка!\n'
                                                 'Пожалуйста, повторите свой запрос в корректном формате:',
                                            reply_markup=keyboard.back())
                self.bot.register_next_step_handler(msg, enter_question)
            else:
                if message.content_type == 'photo':
                    file_info = self.bot.get_file(message.photo[-1].file_id)
                    downloaded_file = self.bot.download_file(file_info.file_path)
                    question_data = downloaded_file
                else:
                    question_data = None

                # Send request to admins
                db.messages_add((message.chat.id, datetime.now(), False, message.text, question_data))
                cur_user.info['unread'] = "True"
                db.users_update_info(cur_user.id, "info", json.dumps(cur_user.info))

                self.bot.send_message(chat_id=message.chat.id,
                                      text='Ваш запрос успешно отправлен админам!',
                                      reply_markup=cur_keyboard())

        def start_cmp_info_game(message):
            cur_user = self.get_user(message.chat.id)

            if cur_user.role is None:
                # if user not registered (no code)
                cur_keyboard = keyboard.menu
            else:
                # if user registered (yes code)
                cur_keyboard = keyboard.menu_reg

            if message.text == '<< Назад':
                self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
                                      reply_markup=cur_keyboard())
            elif message.text == '▶️ СТАРТ':
                db.users_update_info(message.chat.id, 'status', 'Информация о компании - страница 1')
                self.bot.send_message(chat_id=message.chat.id,
                                      text='Линейка товаров пива компании BeerCoders - это искусство пивоварения, которое сочетает в себе традиционные методы и инновационные технологии. Наша продукция включает в себя широкий ассортимент пива, от классических сортов до экспериментальных новинок, которые удивят даже самых искушенных ценителей пива.\n\nВопрос: Как вы думаете, сколько литров пива наша компания производит за 1 месяц?',
                                      reply_markup=keyboard.cmp_info_game_1())
            else:
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Неизвестная команда!',
                                            reply_markup=keyboard.start_btn())
                self.bot.register_next_step_handler(msg, start_cmp_info_game)

        def training_again(message):
            cur_user = self.get_user(message.chat.id)

            if message.text == '<< Назад':
                self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
                                      reply_markup=keyboard.menu_reg())
            elif message.text == 'Пройти еще раз':
                db.users_update_info(message.chat.id, 'status', 'Обучение обязанностям - страница 1')
                db_duties = db.get_duties_by_role_id(cur_user.role)
                self.duties = [Duty(id=db_duty[0],
                                    name=db_duty[1],
                                    about=db_duty[2],
                                    question=db_duty[3],
                                    answers=db_duty[4]) for db_duty in db_duties]
                self.bot.send_message(chat_id=message.chat.id,
                                      text=f'Обязанность №1: {self.duties[0].name}\n\nОписание: {self.duties[0].about}\n\nВопрос: {self.duties[0].question}',
                                      reply_markup=keyboard.duties_training(0, self.duties[0].answers))
            else:
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Неизвестная команда!',
                                            reply_markup=keyboard.training_again())
                self.bot.register_next_step_handler(msg, training_again)

        # users profile main page
        def profile_main_page(message):
            cur_user = db.users_get_one(message.chat.id)

            if message.text == '<< Назад':
                self.bot.send_message(message.from_user.id, 'Главное меню! 🍺',
                                      reply_markup=keyboard.menu_reg())
            elif message.text == '🍺 Запросить выдачу пива':
                if cur_user[3] == 0:
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text='У Вас еще нет пива :(',
                                                reply_markup=keyboard.profile())
                    self.bot.register_next_step_handler(msg, profile_main_page)

                else:
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text='Ваше пиво:',
                                                reply_markup=keyboard.profile())
                    msg = self.bot.send_animation(chat_id=message.chat.id,
                                                  animation=open(os.path.join(path, 'static', 'beer.gif'), 'rb'))

                    db.users_update_info(cur_user[0], 'beer_amount', cur_user[3] - 1)
                    self.bot.register_next_step_handler(msg, profile_main_page)

            elif message.text == '🖼 Моя карточка':

                if cur_user[4] == '' and cur_user[5] is None:
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text='Ваша карточка не заполнена',
                                                reply_markup=keyboard.card_setup())
                elif cur_user[5] is None:
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text=cur_user[4],
                                                reply_markup=keyboard.card_setup())

                else:
                    msg = self.bot.send_photo(chat_id=message.chat.id,
                                              caption=cur_user[4],
                                              photo=cur_user[5],
                                              reply_markup=keyboard.card_setup())
                self.bot.register_next_step_handler(msg, profile_main_page)
            else:
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Неизвестная команда!',
                                            reply_markup=keyboard.training_again())
                self.bot.register_next_step_handler(msg, training_again)

        def edit_profile_about(message):

            if message.text == '<< Назад':
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Ваш профиль:',
                                            reply_markup=keyboard.profile())
                self.bot.register_next_step_handler(msg, profile_main_page)

            else:
                db.users_update_info(message.chat.id, 'about', message.text)
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Текст обновлен',
                                            reply_markup=keyboard.profile())
                self.bot.register_next_step_handler(msg, profile_main_page)

        def edit_profile_photo(message):

            if message.text == '<< Назад':
                msg = self.bot.send_message(chat_id=message.chat.id,
                                            text='Ваш профиль:',
                                            reply_markup=keyboard.profile())
                self.bot.register_next_step_handler(msg, profile_main_page)

            else:
                if message.content_type != 'photo':
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text='Вы отправили не фото')
                    self.bot.register_next_step_handler(msg, edit_profile_photo)
                else:
                    file_id = message.photo[-1].file_id
                    file_info = self.bot.get_file(file_id)
                    downloaded_file = self.bot.download_file(file_info.file_path)
                    db.users_update_info(message.chat.id, 'photo', downloaded_file)
                    msg = self.bot.send_message(chat_id=message.chat.id,
                                                text='Фото обновлено',
                                                reply_markup=keyboard.profile())
                    self.bot.register_next_step_handler(msg, profile_main_page)

        # ---------------------------------------------------------------------------------------------------------------------
        # Inline buttons

        # Some functions for processing of incoming text messages
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_query(call):
            try:
                cur_user = self.get_user(call.message.chat.id)

                if len(call.data.split('|')) == 2:
                    prefix, data = call.data.split('|')
                else:
                    prefix, data, answ = call.data.split('|')

                if prefix == 'cmp_info_game':
                    if data == '1':
                        db.users_update_info(call.message.chat.id, 'status', 'Информация о компании - страница 2')
                        # Вопрос 1
                        if answ == 'True':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 1/3\n\nЛинейка товаров пива компании BeerCoders - это искусство пивоварения, которое сочетает в себе традиционные методы и инновационные технологии. Наша продукция включает в себя широкий ассортимент пива, от классических сортов до экспериментальных новинок, которые удивят даже самых искушенных ценителей пива.\n\nВопрос: Как вы думаете, сколько литров пива наша компания производит за 1 месяц?\n\nОтвет: Действительно, наша компания производит 40 тонн пива каждый месяц, что позволяет многим людям пить пиво каждый день :)\n\nВам начислено +4 пива!',
                                                       reply_markup=keyboard.cmp_info_game_1_answer())
                            self.bot.answer_callback_query(call.id, 'Правильно!\n'
                                                                    'Вы получили бутылку пива!', show_alert=True)
                            cur_user.beer_amount += 1
                            db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)

                        elif answ == 'False':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 1/3\n\nЛинейка товаров пива компании BeerCoders - это искусство пивоварения, которое сочетает в себе традиционные методы и инновационные технологии. Наша продукция включает в себя широкий ассортимент пива, от классических сортов до экспериментальных новинок, которые удивят даже самых искушенных ценителей пива.\n\nВопрос: Как вы думаете, сколько литров пива наша компания производит за 1 месяц?\n\nОтвет: Действительно, наша компания производит 40 тонн пива каждый месяц, что позволяет многим людям пить пиво каждый день :)',
                                                       reply_markup=keyboard.cmp_info_game_1_answer())
                        elif answ == 'next':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 2/3\n\nВода - она есть везде, даже в пиве. Используемая в пивоварении вода должна быть качественной и чистой. От качества воды зависит вкус пива.\n\nВопрос: Как Вы думаете, какой процент от объема пива занимает вода?',
                                                       reply_markup=keyboard.cmp_info_game_2())
                    elif data == '2':
                        db.users_update_info(call.message.chat.id, 'status', 'Информация о компании - страница 3')
                        # Вопрос 2
                        if answ == 'True':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 2/3\n\nВода - она есть везде, даже в пиве. Используемая в пивоварении вода должна быть качественной и чистой. От качества воды зависит вкус пива.\n\nВопрос: Как Вы думаете, какой процент от объема пива занимает вода?\n\nОтвет: Вы действительно правы, 95% - именно такое процентное содержание воды в нашем пиве. При изготовлении сортов нашего пива используется вода из подземных источников, расположенных на глубине до 200 метров\n\nВам начислено +4 пива!',
                                                       reply_markup=keyboard.cmp_info_game_2_answer())

                            self.bot.answer_callback_query(call.id, 'Правильно!\n'
                                                                    'Вы получили бутылку пива!', show_alert=True)
                            cur_user.beer_amount += 1
                            db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)

                        elif answ == 'False':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 2/3\n\nВода - она есть везде, даже в пиве. Используемая в пивоварении вода должна быть качественной и чистой. От качества воды зависит вкус пива.\n\nВопрос: Как Вы думаете, какой процент от объема пива занимает вода?\n\nОтвет: 95% - именно такое процентное содержание воды в нашем пиве. При изготовлении сортов нашего пива используется вода из подземных источников, расположенных на глубине до 200 метров',
                                                       reply_markup=keyboard.cmp_info_game_2_answer())
                        elif answ == 'next':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 3/3\n\nBeerCoders - это искусство пивоварения, которое сочетает в себе традиционные методы и инновационные технологии. Наша линейка товаров включает в себя пиво с яркими фруктовыми нотками, пиво с глубокими карамельными оттенками, пиво с яркими хмелевыми нотками и многое другое. Мы также предлагаем эксклюзивные сорта пива, которые доступны только в наших пивных барах.\n\nВопрос: Как Вы считаете, какое самое вкусное пиво?',
                                                       reply_markup=keyboard.cmp_info_game_3())
                    elif data == '3':
                        db.users_update_info(call.message.chat.id, 'status', 'Информация о компании - страница 3')
                        # Вопрос 3
                        if answ == 'True':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 3/3\n\nBeerCoders - это искусство пивоварения, которое сочетает в себе традиционные методы и инновационные технологии. Наша линейка товаров включает в себя пиво с яркими фруктовыми нотками, пиво с глубокими карамельными оттенками, пиво с яркими хмелевыми нотками и многое другое. Мы также предлагаем эксклюзивные сорта пива, которые доступны только в наших пивных барах.\n\nВопрос: Как Вы считаете, какое самое вкусное пиво?\n\nОтвет: На самом деле это вопрос с подвохом, пиво - оно есть пиво, поэтому все виды пива - самые лучшие ;)\n\nВам начислено +4 пива!',
                                                       reply_markup=keyboard.cmp_info_game_3_answer())

                            self.bot.answer_callback_query(call.id, 'Правильно!\n'
                                                                    'Вы получили бутылку пива!', show_alert=True)
                            cur_user.beer_amount += 1
                            db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)

                        elif answ == 'False':
                            self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                       message_id=call.message.id,
                                                       text='Вопрос 3/3\n\nОтвет: ...',
                                                       reply_markup=keyboard.cmp_info_game_3_answer())

                        # elif answ == 'next':
                        #     self.bot.edit_message_text(chat_id=call.message.chat.id,
                        #                            message_id=call.message.id,
                        #                            text=f'Молодцы, теперь Вы ознакомлены с нашей компанией!',
                        #                            reply_markup=keyboard.cmp_info_game_3())
                    elif data == 'end':
                        db.users_update_info(call.message.chat.id, 'status', 'Информация о компании - завершил')
                        cur_user.beer_amount += 5
                        db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)
                        self.bot.send_message(chat_id=call.message.chat.id, text='Подробнее ознакомиться с компанией '
                                                                                 'вы можете на сайте https://dym-dino.ru\n\n'
                                                                                 'А пока мы вам выдали 5 бутылок пива!')
                        # Завершить игру
                        cur_user = self.get_user(call.message.chat.id)

                        self.bot.delete_message(chat_id=call.message.chat.id,
                                                message_id=call.message.id)

                        if cur_user.role is None:
                            # if user not registered (no code)
                            self.bot.send_message(call.message.chat.id, 'Главное меню! 🍺',
                                                  reply_markup=keyboard.menu())
                        else:
                            # if user registered (yes code)
                            self.bot.send_message(call.message.chat.id, 'Главное меню! 🍺',
                                                  reply_markup=keyboard.menu_reg())
                elif prefix == 'duties_training':
                    if answ in ['True', 'False']:
                        self.bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                           message_id=call.message.id,
                                                           reply_markup=keyboard.duties_training_answ(int(data),
                                                                                                      self.duties[
                                                                                                          int(data)].answers,
                                                                                                      len(self.duties)))
                        if answ == 'True':
                            self.bot.answer_callback_query(call.id, 'Правильно!\n'
                                                                    'Вы получили бутылку пива!', show_alert=True)
                            cur_user.beer_amount += 1
                            db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)

                    elif answ == 'next':
                        next_id = int(data) + 1
                        db.users_update_info(call.message.chat.id, 'status',
                                             f'Обучение обязанностям - страница {next_id + 1}')
                        self.bot.edit_message_text(chat_id=call.message.chat.id,
                                                   message_id=call.message.id,
                                                   text=f'Обязанность №{next_id + 1}: {self.duties[next_id].name}\n\nОписание: {self.duties[next_id].about}\n\nВопрос: {self.duties[next_id].question}',
                                                   reply_markup=keyboard.duties_training(next_id,
                                                                                         self.duties[next_id].answers))
                    elif answ == 'end':
                        cur_user = self.get_user(call.message.chat.id)
                        cur_user.info['training_done'] = True
                        db.users_update_info(call.message.chat.id, 'status', 'Обучение обязанностям - завершено')
                        db.users_update_info(call.message.chat.id, 'info', json.dumps(cur_user.info))

                        self.bot.delete_message(chat_id=call.message.chat.id,
                                                message_id=call.message.id)

                        self.bot.send_message(call.message.chat.id,
                                              'Вы закончили обучение!\nВам начислено 5 бутылок пива!',
                                              reply_markup=keyboard.menu_reg())
                        cur_user.beer_amount += 5
                        db.users_update_info(cur_user.id, 'beer_amount', cur_user.beer_amount)

                elif prefix == 'card_setup':
                    self.bot.clear_step_handler_by_chat_id(call.message.chat.id)
                    if data == 'about':
                        msg = self.bot.send_message(chat_id=call.message.chat.id,
                                                    text='Введите новое описание',
                                                    reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, edit_profile_about)

                    elif data == 'photo':
                        msg = self.bot.send_message(chat_id=call.message.chat.id,
                                                    text='Отправьте новое фото',
                                                    reply_markup=keyboard.back())
                        self.bot.register_next_step_handler(msg, edit_profile_photo)

                elif prefix == 'often_questions':
                    db_questions = db.questions_get_one(int(data))
                    self.bot.send_message(chat_id=call.message.chat.id,
                                          text=f'Вопрос: {db_questions[1]}\nОтвет: {db_questions[2]}',
                                          reply_markup=keyboard.menu_reg())
                elif prefix == 'nav_bar':
                    db_users = db.users_get_all()
                    db_users = [i for i in db_users if i[1] is not None]
                    db_users.sort(key=lambda x: x[0])

                    if answ == 'next':
                        if int(data) + 1 < len(db_users):
                            id = int(data) + 1
                        else:
                            id = 0
                    elif answ == 'back':
                        if int(data) - 1 >= 0:
                            id = int(data) - 1
                        else:
                            id = len(db_users) - 1
                    else:
                        return

                    role = db.roles_get_one(db_users[id][1])[1]
                    self.bot.delete_message(chat_id=call.message.chat.id,
                                            message_id=call.message.id)
                    if db_users[id][5] is not None:
                        self.bot.send_photo(chat_id=call.message.chat.id,
                                            photo=db_users[id][5],
                                            caption=f'Описание: {db_users[id][4] if  len(db_users[id][4]) > 0 else "тут пока пусто :("}\nДолжность: {role}\n{get_name(db_users[id][-1])}',
                                            reply_markup=keyboard.nav_bar(id, len(db_users)),
                                            parse_mode='HTML')
                    else:
                        self.bot.send_message(chat_id=call.message.chat.id,
                                              text=f'Описание: {db_users[id][4] if  len(db_users[id][4]) > 0 else "тут пока пусто :("}\nДолжность: {role}\n{get_name(db_users[id][-1])}',
                                              reply_markup=keyboard.nav_bar(id, len(db_users)),
                                              parse_mode='HTML')

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
