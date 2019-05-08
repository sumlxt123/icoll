#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


"""
邮件发送模块，使用多进程方式，减少资源浪费
"""


from flask import render_template,current_app
from flask_mail import Mail,Message
from threading import Thread

mail = Mail()

def send_async_email(app,msg):
    """邮件发送函数"""
    with app.app_context():
        mail.send(msg)
        # app.logger.info('向用户 {0} 发送邮件成功'.format(msg.recipients))
        # app.logger.debug('邮件内容 {0} '.format(msg.html))


def send_mail(to, subject, template, **kwargs):
    app = current_app._get_current_object()  # 代理获取到原始对象，传递给子线程的上下文
    # 应用上下文
    msg = Message(subject=subject,  # 主题内容
                  sender=app.config['FLASKY_MAIL_SENDER'],  # 发送邮件的地址
                  recipients=[to,app.config['FLASKY_MAIL_SENDER']],  # 为列表，包含所有收件人
                  html=render_template(template + '.html', **kwargs)  # 使用模板，装饰内容
                  )  # 实例化一个消息对象，准备发送邮件，接收者

    # msg.body = render_template(template+'.txt', **kwargs)
    # msg.html = render_template(template+'.html', **kwargs)

    # 使用多线程给用户发邮件，否则注册页面会出现卡顿的情况
    th = Thread(target=send_async_email, args=[app,msg])
    th.start()
    return 'ok'
