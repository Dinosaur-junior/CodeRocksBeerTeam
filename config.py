# -*- coding: utf-8 -*-
# It's a Telegram bot (config script)

# Written by Dinosaur
#                __
#               / _)
#      _.----._/ /
#     /         /
#  __/ (  | (  |
# /__.-'|_|--|_|


# ---------------------------------------------------------------------------------------------------------------------
# import libraries

import os
import sys

import pytz

# ---------------------------------------------------------------------------------------------------------------------
# configuration

# bot token
BOT_TOKEN = '6209088703:AAGIaIi_S5EIBAU3Y3yMIOpGQAoghlsw508'

# database info
DATABASE_INFO = {'database': 'beer', 'host': '89.108.78.64', 'user': 'beer',
                 'password': 'BeerWillSaveTheWorld!!!', 'port': 5432}

# timezone
TZ = pytz.timezone('Europe/Moscow')

# path to the script
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
