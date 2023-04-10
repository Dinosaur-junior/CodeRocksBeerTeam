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
from functools import wraps

from flask import Flask, render_template, send_from_directory, Response, request

import config
from config import path
from database import Database
from funcitons import print_error

# ---------------------------------------------------------------------------------------------------------------------
# CONFIG

# connect to database
db = Database

# flask app
app = Flask(__name__, static_folder=os.path.join(path, 'static'), template_folder=os.path.join(path, 'templates'))
app.config['SECRET_KEY'] = config.FLASK_SECRET_KEY


# --------------------------------------------------------------------------------------------------------------------
# CHECK AUTH

# check auth function
def check_auth(username, password):
    if username == config.ADMIN_LOGIN and password == config.ADMIN_PASSWORD:
        return True
    else:
        return False


# login page
def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


# authenticate decorator
def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if auth is None:
            return authenticate()

        if not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


# ---------------------------------------------------------------------------------------------------------------------
# ROUTES

# favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


# error page
@app.errorhandler(Exception)
def all_exception_handler(error):
    print_error(error)
    return render_template('error.html')


# main page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


# production info
@app.route('/production', methods=['GET'])
def production():
    images = [i for i in os.listdir(os.path.join(path, 'static')) if 'production' in i]
    return render_template('production.html', images=images, images_i=[i for i in range(1, len(images))])


# products info
@app.route('/products', methods=['GET'])
def products():
    images = [i for i in os.listdir(os.path.join(path, 'static')) if 'product' in i and 'production' not in i]
    return render_template('products.html', images=images, images_i=[i for i in range(1, len(images))])


# admin panel
@app.route('/admin', methods=['GET', 'POST'])
@requires_auth
def admin():
    return render_template('admin.html')


# ---------------------------------------------------------------------------------------------------------------------
# starting the web server
if __name__ == '__main__':
    while True:
        try:
            app.run(host='0.0.0.0', threaded=True, debug=True)
        except Exception as e:
            print(e)
