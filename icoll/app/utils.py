#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
# 工具文件，自定义日志，自定义错误类，自定义装饰器
>[日志及自定义错误类](https://www.jianshu.com/p/9f08c72a148b?t=1512884592639)

"""

import os
import logging
from logging.handlers import RotatingFileHandler


class LogConfig(object):
    """自定义日志类的默认配置，实现自动加载"""
    _BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    _FORMATTER = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] "
                                  "- %(levelname)s: %(message)s")  # 日志格式
    _LOG_LEVEL = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR
    }# 定义默认日志级别
    _LOG_FILE_MAX_BYTES = 100 * 1024 * 1024  # 定义单个日志文件默认大小
    _LOG_FILE_BACKUP_COUNT = 3  # 定义日志文件，轮转数量是 10 个
    _LOG_PATH = os.path.join(_BASE_DIR, 'logs')
    _LOG_FILE = {
        logging.DEBUG: os.path.join(_LOG_PATH, 'debug.log'),
        logging.INFO: os.path.join(_LOG_PATH, 'info.log'),
        logging.WARNING: os.path.join(_LOG_PATH, 'info.log'),
        logging.ERROR: os.path.join(_LOG_PATH, 'error.log')
    }




    @classmethod
    def set_logconfig(cls,name=None,level=None,formatter=None,logpath=None,console_in:bool=True):
        """定义日志记录器，定义文件处理器，定义控制台处理器，然后将记录器添加到处理器中"""
        if isinstance(name,str):
            name = 'root'
        logger = logging.getLogger(name)

        # 定义日志级别
        if not level or not (level in [log_level for log_level in cls._LOG_LEVEL.keys()]):
            logger.setLevel(cls._LOG_LEVEL['debug'])
        else:
            logger.setLevel(cls._LOG_LEVEL[level])

        # 定义文件处理器,当未传入文件路径时，按默认设置获取路径
        if not formatter or not isinstance(formatter, logging.Formatter):  # 处理日志格式
            formatter = cls._FORMATTER
        else:
            raise ValueError('formatter value:[{}] not is '  # 考虑到日志无法正常输出时查找原因，
                             'logging.Formatter object.'.format(formatter))  # 还是配置可见比较靠谱
        if logpath:  # 日志文件路径
            if not os.path.exists(logpath): os.mkdir(logpath)
            cls._LOG_PATH = logpath
        if not os.path.exists(cls._LOG_PATH): os.mkdir(cls._LOG_PATH)  # 检查日志目录是否存在，不存在则创建

        cls._set_filehandler(logger, cls._LOG_FILE[logger.level],
                             logger.level, formatter)  # 创建文件处理器

        # 创建控制台处理器,当console_in 为假，不从控制台输出日志，默认从控制台输出
        if console_in:
            cls._set_streamhandler(logger,logger.level, formatter)  # 创建控制台处理器

        # return logger


    @staticmethod
    def _set_filehandler(logger,filename,level,formatters):
        """设置文件处理器"""
        if not logger.handlers:  # 对handlers列表进行判断，为空则添加处理器，否则直接写日志，避免重复写入日志的问题
            fh = RotatingFileHandler(filename=filename)
            fh.setLevel(level)
            fh.setFormatter(formatters)
            logger.removeHandler(fh)  # 移除重复日志
        return logger


    @staticmethod
    def _set_streamhandler(logger,level,formatters):
        """设置文件处理器"""
        if not logger.handlers:  # 对handlers列表进行判断，为空则添加处理器，否则直接写日志，避免重复写入日志的问题
            ch = logging.StreamHandler()
            ch.setLevel(level)
            ch.setFormatter(formatters)
            logger.removeHandler(ch)  # 移除重复日志
        return logger





#--------------------------------
#----方法二
#--------------------------------
from logging.config import dictConfig

log_cofig = {
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] [%(filename)s-%(lineno)s line] [%(levelname)s]: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
}

# dictConfig(log_cofig)






if __name__ == "__main__":
    LogConfig.set_logconfig(name='icoll',level='info')
    LogConfig.set_logconfig(name='icoll',level='debug')

