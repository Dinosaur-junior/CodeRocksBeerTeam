# -*- coding: utf-8 -*-
# It's a Telegram bot (mailing class)


# ---------------------------------------------------------------------------------------------------------------------
# import libraries
import datetime
import io
import time
from threading import Thread

from funcitons import print_error


# ---------------------------------------------------------------------------------------------------------------------
# MAILING CLASS
class Mailing(Thread):
    def __init__(self, mail_users, text, files, bot, mime, filename, keyboard):
        Thread.__init__(self)
        self.work = 0
        self.users = mail_users
        self.text = text
        self.files = files
        self.bot = bot
        self.send = []
        self.problem_chats = []
        self.mime = mime
        self.filename = filename
        self.time = datetime.datetime.now().strftime('%H:%M - %d.%m.%Y')
        self.keyboard = keyboard

    def run(self):
        self.work = 1

        if self.files is None or len(self.files) < 5:
            for chat in self.users:
                try:
                    self.bot.send_message(chat[0], self.text, reply_markup=self.keyboard)
                    time.sleep(1)
                    self.send.append(chat)
                except Exception as e:
                    print_error(e)
                    self.problem_chats.append(chat)

        else:
            if 'image' in self.mime:
                for chat in self.users:
                    try:
                        self.bot.send_photo(chat[0], photo=self.files, caption=self.text, reply_markup=self.keyboard)
                        time.sleep(1)
                        self.send.append(chat)
                    except Exception as e:
                        print_error(e)
                        self.problem_chats.append(chat)

            elif 'video' in self.mime:
                for chat in self.users:
                    try:
                        self.bot.send_video(chat[0], video=self.files, caption=self.text, reply_markup=self.keyboard)
                        time.sleep(1)
                        self.send.append(chat)
                    except Exception as e:
                        print_error(e)
                        self.problem_chats.append(chat)

            else:
                for chat in self.users:
                    try:
                        file = io.BytesIO(self.files)
                        file.name = self.filename
                        self.bot.send_document(chat[0], document=file, caption=self.text, reply_markup=self.keyboard)
                        time.sleep(1)
                        self.send.append(chat)
                    except Exception as e:
                        print_error(e)
                        self.problem_chats.append(chat)

        self.work = 0

    def stop(self):
        self.work = 0
