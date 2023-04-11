# -*- coding: utf-8 -*-
# It's a Telegram bot (init script)

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

from database import Database

# ---------------------------------------------------------------------------------------------------------------------
# initialization

# path to the script
path = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.path.dirname(os.path.realpath(__file__))

# database
db = Database()