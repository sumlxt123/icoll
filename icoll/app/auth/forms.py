#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
定义用户相关的表单
"""


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    """用户登录表单"""
    username = StringField(label=u'用户名或邮箱', validators=[DataRequired(),])
    password = PasswordField(label=u'密码', validators=[DataRequired(),])
    submit = SubmitField(label=u'登录')



class RegisterForm(FlaskForm):
    """用户注册表单"""
    username = StringField(label=u'用户名',validators=[DataRequired(), Length(1,64),
            Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'用户名必须是字母与数字的组合')],
                           id='registerlength')
    password = PasswordField(label=u'密码',validators=[DataRequired(),
                            EqualTo('password2', message=u'两次密码必须相同')], id='registerlength')
    password2 = PasswordField(label=u'确认密码',validators=[DataRequired()], id='registerlength')
    email = StringField(label=u'邮箱地址',validators=[DataRequired(), Length(1,64), Email()], id='registerlength')
    submit = SubmitField(label=u'马上注册')


    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise  ValidationError("Email 已注册过")


    def validata_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已存在，请使用其他用户名')

