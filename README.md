# py16-project

#### 项目介绍
Python16开发班项目示例

#### 软件架构
软件架构说明


####项目目录结构
web
├── manage.py
├── myadmin
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── myhome
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── static
├── templates
└── web
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

在项目中头像上传时,使用的地址
为什么有些地方写 /static/uploads/
有些地方写 ./static/uploads/
甚至  /home/yc/py16/py16-project/web/static/uploads/

地址的使用,分两种情况
一种是系统的文件操作 可以使用 ./static/uploads/ 或者 /home/yc/py16/py16-project/web/static/uploads/

一种是给服务器使用,浏览器访问时使用 /static/uploads/ 因为此处 / 代表当前服务器地址 http://127.0.0.1:8000

127.0.0.1
locahost

location.href = /index/


分页优化解决方案

1,自定义模板标签



#### 安装教程

1. xxxx
2. xxxx
3. xxxx

#### 使用说明

1. xxxx
2. xxxx
3. xxxx

#### 参与贡献

1. Fork 本项目
2. 新建 Feat_xxx 分支
3. 提交代码
4. 新建 Pull Request


#### 码云特技

1. 使用 Readme\_XXX.md 来支持不同的语言，例如 Readme\_en.md, Readme\_zh.md
2. 码云官方博客 [blog.gitee.com](https://blog.gitee.com)
3. 你可以 [https://gitee.com/explore](https://gitee.com/explore) 这个地址来了解码云上的优秀开源项目
4. [GVP](https://gitee.com/gvp) 全称是码云最有价值开源项目，是码云综合评定出的优秀开源项目
5. 码云官方提供的使用手册 [https://gitee.com/help](https://gitee.com/help)
6. 码云封面人物是一档用来展示码云会员风采的栏目 [https://gitee.com/gitee-stars/](https://gitee.com/gitee-stars/)