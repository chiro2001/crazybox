就算有很方便的QQ作人与人间的互相联系，但是我还是享受自己创造这种联系的载体的成就感。
<h3>工程开源地址：</h3>
<a href="https://github.com/LanceLiang2018/chatroom">https://github.com/LanceLiang2018/chatroom</a>

<h3>使用方法</h3>
1、文件内容：

<img class="alignnone size-medium wp-image-84" src="http://lanceliang2018.xyz/wp-content/uploads/1-300x139.jpg" alt="" width="300" height="139" />

database.db    和用户设置有关的数据库

entries.db    储存聊天记录的数据库

db_init.py    对数据库清空and初始化(debug)

db_list.py    列出数据库的所有内容(debug)

database.py    处理数据库有关操作

sever.py    服务器

templates/    Html的模板

2、开启服务器：

Linux：screen python3 sever.py    或者    python3 sever.py &amp;    (会有回显)

Windows：python sever.py

3、更改端口：

修改sever.py最后一行，aapp.run(port=&lt;int:port&gt;)

2018/10/28 修正

textarea高度自适应

右下角加入小玩意

加入浏览量统计(不过只有一个统计)

祝大家都开心。

### 更新

https://lance-chatroom.herokuapp.com/

上面是heroku的托管。

加入wap页面切换，老人机也可以为所欲为。