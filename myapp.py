from flask import *


def init():
    global app
    app = Flask(__name__)
    app.secret_key = 'JIL:HUKHDUKHKJ:hi;sUDFilusmfudifyniUy'
    # print(dir(app))


def get_app():
    return app
