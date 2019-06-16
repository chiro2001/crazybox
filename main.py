from flask import *
import os
import myapp
import markdown

myapp.init()
app = myapp.get_app()


from chatroom import *
from wenku8 import *
from go import *


@app.route('/')
def crazybox_index():
    with open('README.md', encoding='utf8') as f:
        data = markdown.markdown(f.read())
        return data


if __name__ == '__main__':
    app.run(threaded=True, debug=False, host='0.0.0.0', port=os.getenv("PORT", "5000"))
