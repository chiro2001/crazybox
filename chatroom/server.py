from flask import Flask, session, redirect, url_for, escape, request, render_template
import hashlib
from chatroom.database import *
from chatroom.db_init import clear_all
import time
import threading
import os
import pytz
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr


_app_name = 'chatroom'
_app_base = '/%s' % _app_name


# app = Flask(__name__)
# from main import app
import myapp
# myapp.init()
app = myapp.get_app()

# entries = []
users = []


def get_icon(email):
    return'https://s.gravatar.com/avatar/' + hashlib.md5(email.encode()).hexdigest() + '?s=144'


@app.route(_app_base + '/', methods=['GET'])
def to_index():
    return redirect(_app_base + '/index')


@app.route(_app_base + '/<string:room>', methods=['GET', 'POST'])
def index(room: str):
    sever_init()
    if request.method == 'GET':
        entries = list(entry_get(room, 0))
        for k in range(len(entries)):
            entries[k] = list(entries[k])
            s = entries[k][4]
            line = s.split('\n')
            sumi = 0
            for j in line:
                sumi = sumi + len(j) // 35
            entries[k].append(entries[k][4].count('\n') + sumi)

        if 'username' not in session:
            return redirect(url_for('login'))
        if 'display_mode' in session and session['display_mode'] == 'wap':
            html = 'ChatRoom_wap.html'
        else:
            html = 'ChatRoom.html'
        return render_template(_app_name + '/' + html, username=session['username'],
                               icon=session['icon'],
                               entries=entries,
                               users=users,
                               title=room,
                               room=room,
                               app_base=_app_base,
                               )
    if request.method == 'POST':
        timedata = time.localtime(time.time())
        cndata = datetime(timedata[0], timedata[1], timedata[2], timedata[3], timedata[4], timedata[5])
        central = pytz.timezone('Asia/Shanghai')
        time_cn = central.localize(cndata)
        data = {
            'username': session['username'],
            'message': request.form['message'],
            'time': str(time_cn.month).zfill(2) + '/' + str(time_cn.day).zfill(2) + ' ' + \
                    str(time_cn.hour).zfill(2) + ':' + str(time_cn.minute).zfill(2),
        }
        entry_insert(entry_get_new_id(), data['username'], data['time'],
                     get_icon(session['email']), data['message'], room)
        if session['email'].lower() == 'lanceliang2018@163.com' and 'special' in room.lower():
            my_sender = 'LanceLiang2018@163.com'  # 发件人邮箱账号
            my_pass = '1352040930smtp'  # 发件人邮箱密码
            # my_user = '1352040930@qq.com'  # 收件人邮箱账号
            users_ = user_all()
            users_to_send = []
            for user in users_:
                if '_' in user[0]:
                    users_to_send.append(user)
            for user in users_to_send:
                try:
                    # print('try to send:', user)
                    msg = MIMEText(data['message'], 'plain', 'utf-8')
                    msg['From'] = formataddr(["Lance Liang", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                    msg['To'] = formataddr([user[0], user[1]])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                    msg['Subject'] = "来自 Lance 的新消息"  # 邮件的主题，也可以说是标题

                    server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
                    server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                    server.sendmail(my_sender, [user[1], ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                    server.quit()  # 关闭连接
                except Exception as e:
                    print(e)
        # 接受消息。
        if '_' in session['username'] and 'special' in room.lower():
            my_sender = 'LanceLiang2018@163.com'  # 发件人邮箱账号
            my_pass = '1352040930smtp'  # 发件人邮箱密码
            # my_user = '1352040930@qq.com'  # 收件人邮箱账号
            try:
                # print('try to send:', user)
                msg = MIMEText(data['message'], 'plain', 'utf-8')
                msg['From'] = formataddr(["Lance Liang", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
                msg['To'] = formataddr(['Lance Liang', my_sender])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
                msg['Subject'] = "来自 %s 的新消息" % session['username']  # 邮件的主题，也可以说是标题

                server = smtplib.SMTP_SSL("smtp.163.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465
                server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
                server.sendmail(my_sender, [my_sender, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
                server.quit()  # 关闭连接
            except Exception as e:
                print(e)

        return redirect(_app_base + '/%s' % room)


@app.route(_app_base + '/wap', methods=['GET'])
def wap():
    session['display_mode'] = 'wap'
    return redirect(_app_base + '/')


@app.route(_app_base + '/pc', methods=['GET'])
def pc():
    session['display_mode'] = 'pc'
    return redirect(_app_base + '/')


@app.route(_app_base + '/signup', methods=['GET', 'POST'])
def signup():
    if 'username' in session:
        redirect(url_for('logout'))
    if request.method == 'POST':
        if request.form['passwd'] != request.form['passwd_']:
            return '两次密码不一致。' + '<a href=%s>返回</a>' % url_for('signup')
        if request.form['username'] == '':
            return '用户名不能为空。' + '<a href=%s>返回</a>' % url_for('signup')
        hl = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        result = user_add(request.form['username'], hl, request.form['email'].lower())
        sever_user_init()
        return result + '<a href=%s>首页</a>' % url_for('to_index')
    return render_template(_app_name + '/' + 'signup.html', app_base=_app_base,)


@app.route(_app_base + '/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        redirect(url_for('logout'))
    if request.method == 'POST':
        hl = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        result = user_check(request.form['username'], hl)
        if result != 'Success':
            return result
        session['username'] = request.form['username']
        session['passwd'] = hl
        session['email'] = user_get_email(session['username'])
        session['icon'] = get_icon(session['email'])
        return redirect(url_for('to_index'))
    return render_template(_app_name + '/' + 'login.html', app_base=_app_base)


@app.route(_app_base + '/delete', methods=['GET', 'POST'])
def delete_user():
    if 'username' in session:
        redirect(url_for('logout'))
    if request.method == 'POST':
        if request.form['passwd'] != request.form['passwd2']:
            return '两次密码不正确' + '<a href=%s>返回</a>' % url_for('delete_user')
        hl = hashlib.md5(request.form['passwd'].encode()).hexdigest()
        result = user_del(request.form['username'], hl)
        if result != 'Success':
            return result + '<a href=%s>返回</a>' % url_for('delete_user')
        session.pop('username', None)
        return result + '<a href=%s>首页</a>' % url_for('to_index')
    return render_template(_app_name + '/' + 'delete.html', app_base=_app_base)


@app.route(_app_base + '/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('to_index'))


@app.route(_app_base + '/get_email/<username>')
def get_email(username):
    email = user_get_email(username)
    return email + '<br><img src=\"%s\">' % (get_icon(email))


@app.route(_app_base + '/history/<string:room>/<int:page>', methods=['GET'])
def get_history(room: str, page: int):
    if 'username' not in session:
        return redirect(url_for('login'))
    if request.method == 'GET':
        if 'display_mode' in session and session['display_mode'] == 'wap':
            html = 'History_wap.html'
        else:
            html = 'History.html'
        get_entries = entry_get(room, page)
        return render_template(_app_name + '/' + html, entries=get_entries, room=room,
                               pre_page=url_for('get_history', room=room, page=max(0, page-1)),
                               next_page=url_for('get_history', room=room, page=page+1),
                               app_base=_app_base)


@app.route(_app_base + '/about')
def about():
    return redirect('https://github.com/LanceLiang2018/chatroom')


@app.route(_app_base + '/clear_all')
def clear():
    # clear_all()
    t = threading.Thread(target=clear_all)
    t.setDaemon(True)
    t.start()
    return 'Thread started...'


def sever_user_init():
    global users
    users = user_all_name()


# def sever_entry_init():
#     global entries
#     entries = list(entry_get(0))
#     for i in range(len(entries)):
#         entries[i] = list(entries[i])
#         s = entries[i][4]
#         line = s.split('\n')
#         sum = 0
#         for j in line:
#             sum = sum + len(j) // 35
#         entries[i].append(entries[i][4].count('\n') + sum)


def sever_init():
    sever_user_init()
    # sever_entry_init()


# set the secret key.  keep this really secret:
# app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    sever_init()
    # app.run(threaded=True, debug=False, host='0.0.0.0', port=10086)
    app.run(threaded=True, debug=False, host='0.0.0.0', port=os.getenv("PORT", "5000"))
    print('Started...')
