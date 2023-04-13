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
BOT_TOKEN = '6074037280:AAHXV6rgX0OKmW6yIN9kHj0qPofvUpWjQK4'
#BOT_TOKEN = '6069953990:AAF5DQIFy6xJIbm3zmGw9ifH5rQAJGW4VW4'

# database info
DATABASE_INFO = {'database': 'beer', 'host': '89.108.78.64', 'user': 'beer',
                 'password': 'BeerWillSaveTheWorld!!!', 'port': 5432}

# timezone
TZ = pytz.timezone('Europe/Moscow')

FLASK_SECRET_KEY = 'BeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeer'
ADMIN_LOGIN = 'beer'
ADMIN_PASSWORD = 'beer1234'

# path to the script
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
