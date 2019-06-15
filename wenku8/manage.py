import os
from flask import *
from wenku8.manager import *
import io


# app = Flask(__name__)
import myapp
app = myapp.get_app()

_app_name = 'wenku8'
_app_base = '/%s' % _app_name
# print(_app_base)


@app.route(_app_base + '/', methods=['GET'])
def wenku8_index():
    return '<a href="https://github.com/LanceLiang2018/Wenku8ToEpub-Online">' \
           'https://github.com/LanceLiang2018/Wenku8ToEpub-Online</a>'


@app.route(_app_base + '/cache/<int:book_id>')
def wenku8_cache(book_id: int):
    url = work(book_id)
    return redirect(url)


@app.route(_app_base + '/get/<int:book_id>')
def wenku8_get(book_id: int):
    wk = Wenku8ToEpub()
    filename_ = wk.id2name(book_id)
    if filename_ == '':
        return '没有这个小说！'
    filename = "%s.epub" % filename_
    return redirect('https://light-novel-1254016670.cos.ap-guangzhou.myqcloud.com/%s' % filename)


@app.route(_app_base + '/no_cache/<int:book_id>')
def no_cache(book_id: int):
    wk = Wenku8ToEpub()
    filename_ = wk.id2name(book_id)
    if filename_ == '':
        return '没有这个小说！'
    data = work3(book_id)
    fp = io.BytesIO(data)
    # urlencode方案
    # filename_ = urllib.parse.urlencode({'': filename_})[1:] + '.epub'
    # latin-1 方案
    filename_ = ("%s.epub" % filename_).encode().decode('latin-1')
    response = make_response(send_file(fp, attachment_filename="%s" % filename_))
    response.headers["Content-Disposition"] = "attachment; filename=%s;" % filename_
    return response


if __name__ == '__main__':
    app.run("0.0.0.0", port=int(os.environ.get('PORT', '5000')), debug=False)

