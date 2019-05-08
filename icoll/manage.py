#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
应用启动脚本

第一次初始化数据库：
1.初始化：(venv)  python manage.py db init 这个命令会在项目下创建 migrations 文件夹，所有迁移脚本都存放其中。
2.创建第一个版本：(venv) $ python manage.py db migrate -m "initial migration"  检查migrations\versions，
  会新建一个版本.py，检查里面表格及字段
3.运行升级 (venv) $ python manage.py db upgrade，会把项目使用的数据库文件，更新为新的表格、字段，同时保留数据

迁移数据库
python manage.py db migrate
python manage.py db upgrade

注意：
当报错时：ModuleNotFoundError: No module named 'MySQLdb'
问题原因：
python2和python3在数据库模块支持这里存在区别，python2是mysqldb，而到了python3就变成mysqlclient，
pip install mysqlclient 即可。

或者 添加两行语句也可解决，目前mac是这么解决的
import pymysql
pymysql.install_as_MySQLdb()

"""
import pymysql
pymysql.install_as_MySQLdb()

from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand


from app import create_app,db
from app.models import User

# 初始化应用
# app = create_app('testing')
app = create_app('develop')
# app = create_app('product')

# 配置数据迁移脚本
manager = Manager(app)
manager.add_command('db', MigrateCommand)
migrate = Migrate(app, db)






if __name__ == "__main__":
    # app.run(host='0.0.0.0',port=8000)
    # app.run(host='0.0.0.0',port=5000)
    manager.run()  # 使用此方法启动时，需要添加 runserver 参数