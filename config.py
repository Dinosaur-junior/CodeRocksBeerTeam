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
BOT_TOKEN = 'ber'

# database info
DATABASE_INFO = {''beer'}

# timezone
TZ = pytz.timezone('Europe/Moscow')

FLASK_SECRET_KEY = 'BeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeerBeer'
ADMIN_LOGIN = 'beer'
ADMIN_PASSWORD = 'beer1234'

# path to the script
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))
