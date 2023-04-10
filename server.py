# -*- coding: utf-8 -*-
# Main script
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

from flask import Flask, render_template, send_from_directory

from config import path
from database import Database

# ---------------------------------------------------------------------------------------------------------------------
# CONFIG

# connect to database
db = Database

# flask app
app = Flask(__name__, static_folder=os.path.join(path, 'static'), template_folder=os.path.join(path, 'templates'))


# ---------------------------------------------------------------------------------------------------------------------
# ROUTES

# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.errorhandler(Exception)
def all_exception_handler(error):
    return render_template('error.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# ---------------------------------------------------------------------------------------------------------------------
# starting the web server
if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', threaded=True, debug=True)
        except Exception as e:
            print(e)
