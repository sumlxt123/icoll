#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
配置文件
"""

import os
import logging
import time
from datetime import timedelta
from logging.config import dictConfig


log_cofig = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] [%(filename)s-%(lineno)s line] [%(levelname)s]: %(message)s',
    }},
    'handlers': {
        'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
        },
        'flask.app': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
    },
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class BaseConfig(object):
    """基础配置"""
    DEBUG = False # 默认不开启DEBUG模式
    TESTING = False # 默认不开启TESTING模式
    SECRET_KEY = os.urandom(16)  # 秘钥配置
    # PERMANENT_SESSION_LIFETIME = timedelta(days=31),  # 默认session失效时间一个月
    USE_X_SENDFILE = False  # 不启用X_SENDFILE功能
    LOGGER_NAME = 'icoll'  # 不指定logger名字，使用的是__name__
    # # SERVER_NAME = 'icoll'  # 设置服务器的名字，默认None

    # 此配置导致TypeError: Expected bytes 目前不清楚为什么？？？
    # SESSION_COOKIE_NAME = 'session'  # 设置cookie中的session名字
    MAX_CONTENT_LENGTH = None  # 限制提交请求的最大字节数
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(hours=12)  # 设置文件最大缓存时间
    PREFERRED_URL_SCHEME = 'http'  # 默认的通讯协议
    JSONIFY_MIMETYPE = 'application/json' # 当json数据交互时，设置响应头的mimetype参数


    # 设置数据库配置
    SQLALCHEMY_DATABASE_URI = 'mysql://root:1qaz2wsx3edc@localhost/icoll'  # 配置数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True  # request自动提交db.session.commit()


    # 邮箱配置
    # 126邮箱配置
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'sunlxt123@126.com'
    MAIL_PASSWORD = 'zxcvbnm789'  # （可在环境变量中设置获取）

    # 163邮箱配置
    # MAIL_SERVER = 'smtp.163.com' ＃配置163邮箱的smtp服务，首先你的邮箱要开启smtp服务
    # MAIL_PORT = 465  ＃端口为465
    # MAIL_USE_SSL = True  ＃ TLS服务失败，要用SSL

    # QQ 邮箱配置
    # MAIL_SERVER = 'smtp.qq.com'
    # MAIL_PORT = 25
    # MAIL_USE_TLS = True
    # MAIL_USE_SSL = Flase
    MAIL_DEFAULT_USERNAME = MAIL_USERNAME
    FLASKY_MAIL_SENDER = MAIL_USERNAME

    LOG_PATH = os.path.join(BASE_DIR,'logs')
    LOG_PATH_DEBUG = os.path.join(LOG_PATH,'debug.log')
    LOG_PATH_ERROR = os.path.join(LOG_PATH,'error.log')
    LOG_PATH_INFO = os.path.join(LOG_PATH, 'info.log')
    LOG_FILE_MAX_BYTES = 100 * 1024 * 1024  # 日志文件大小限制
    LOG_FILE_BACKUP_COUNT = 10  # 轮转数量是 10 个


    @staticmethod
    def init_app(app):
        pass





class ProductConfig(BaseConfig):
    """基础配置"""
    DEBUG = False


    @classmethod
    def init_app(cls,app):
        BaseConfig.init_app(app)
        dictConfig(log_cofig)


class DevelopConfig(BaseConfig):
    """基础配置"""
    DEBUG = True


    @classmethod
    def init_app(cls,app):
        BaseConfig.init_app(app)
        dictConfig(log_cofig)



class TestingConfig(BaseConfig):
    """测试配置"""
    DEBUG = True
    # TESTING = True

    @classmethod
    def init_app(cls,app):
        BaseConfig.init_app(app)

        if not os.path.exists(BaseConfig.LOG_PATH): os.mkdir(BaseConfig.LOG_PATH)  # 判断日志存放目录是否存在，不存在则新建
        fh = logging.FileHandler(BaseConfig.LOG_PATH_DEBUG, encoding='UTF-8')  # 设置日志输入文件 handler

        fh.setLevel(logging.DEBUG)
        formatter = ('[%(asctime)s] - [%(filename)s - %(lineno)d line] '
                     '- %(levelname)s: %(message)s')  # 日志输出格式
        fh.setFormatter(logging.Formatter(formatter))
        app.logger.addHandler(fh)

        ch = logging.StreamHandler()  # 设置日志输入文件 handler
        ch.setLevel(logging.INFO)
        formatter = ('[%(asctime)s] - [%(filename)s - %(lineno)d line] '
                     '- %(levelname)s: %(message)s')  # 日志输出格式
        ch.setFormatter(logging.Formatter(formatter))
        app.logger.addHandler(ch)

        # 此两行代码是为了避免日志输出重复的问题
        # app.logger.removeHandler(ch)
        # app.logger.removeHandler(fh)




config = {
    'product': ProductConfig,
    'develop': DevelopConfig,
    'testing': TestingConfig,

    'default': BaseConfig,
}




