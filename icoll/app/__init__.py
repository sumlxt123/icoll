#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


from flask import Flask,current_app
from flask_bootstrap import Bootstrap


# 导入本地模块
from .auth.views import auth,login_manager
from .main.views import main
from .email import mail
from .models import db
from config import config


# 实例化bootstrap
bootstrap = Bootstrap()


# 使用工厂函数初始化蓝图
from werkzeug.utils import import_string

bps = ['app.auth.views:auth',
       'app.main.views:main'
       ]



def create_app(config_name):
    app = Flask(__name__)

    # 初始化配置
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    app.logger.info('app config init secussfull')


    # 初始化应用类
    db.init_app(app)
    mail.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'auth.login'

    # 初始蓝图
    # app.register_blueprint(main)
    # app.register_blueprint(main, url_prefix='/main')  # url_prefix 表示挂载点，一个蓝图可以有多个挂载点
    # app.register_blueprint(auth, url_prefix='/auth')

    # 使用工厂函数初始化蓝图
    for bp_name in bps:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    app.logger.info('app init secussfull')

    return app


