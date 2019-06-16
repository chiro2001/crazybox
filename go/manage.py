import base64
import hashlib
import os

from flask import *
from go.database import DataBase

# app = Flask(__name__)
import myapp
app = myapp.get_app()
_app_name = 'go'
_app_base = '/%s' % _app_name


db = DataBase()


def get_if_in(key: str, form: dict, default=None):
    if key in form:
        return form[key]
    return default


@app.route(_app_base + '/', methods=['GET'])
def go_index():
    return '<a href="https://github.com/LanceLiang2018/Go-Online">https://github.com/LanceLiang2018/Go-Online</a>'


@app.route(_app_base + '/play/<string:code>/', methods=['POST', 'GET'])
def go_play(code: str):
    if request.method == 'GET':
        return jsonify(db.read(code))
    # POST 部分
    form = request.form
    if 'action' not in form:
        return db.make_result(1, message='No action selected')
    action = form['action']
    try:
        if action == 'put':
            player = int(get_if_in('player', form, default=0))
            winner = int(get_if_in('winner', form, default=0))
            default_data = ''
            if 'size' in form:
                size = form['size']
                width = int(size.split('x')[0])
                height = int(size.split('x')[-1])
                default_data = '0' * width
                default_data = default_data + '\n'
                default_data = default_data * height
                default_data = default_data[:-1]
            data = get_if_in('data', form, default=default_data)
            return db.write(code, player, data, winner)

    except Exception as e:
        return db.make_result(1, message='Sever Error', error=str(e))

    return db.make_result(1, message='No supported action')


@app.route(_app_base + '/playing/<string:code>/', methods=['GET'])
def go_playing(code: str):
    return db.read(code)['data']


@app.route(_app_base + '/debug_clear')
def go_clear():
    db.db_init()
    return db.make_result(0)


if __name__ == '__main__':
    app.run("0.0.0.0", port=int(os.environ.get('PORT', '5000')), debug=False)

