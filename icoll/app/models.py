#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

"""
模型定义
定义用户数据模型
"""
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


db = SQLAlchemy()  # 数据库实例化


class User(db.Model,UserMixin):
    """定义用户的数据模型"""
    __tablename__ = 'users'  # 表名

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(64), nullable=False, unique=True)
    # password = Column(String(128), nullable=True,)
    email = Column(String(50), unique=True, nullable=False)
    role_id = db.Column(db.Integer)  # 用于定义用户角色或角色组
    password_hash = db.Column(db.String(128))  # 存储用户加密后的密码
    confirmed = Column(Boolean, default=False)


    def __init__(self, username, password, email):
        self.username = username
        self.password = password.encode('utf')
        self.email = email

    def is_authenticated(self):  # 是否被验证
        return True

    def is_active(self):  # 是否被激活
        return True

    def is_anonymous(self):  # 是否匿名用户
        return False

    def get_id(self):  # 获得用户的ID，并转换Unicode类型
        return self.user_id

    @property
    def password(self):
        """读取用户密码，设置无法读取"""
        raise AttributeError('password is not a read')

    @password.setter
    def password(self,password):
        """设置password属性值，使用加盐加密的方式"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """比较用户密码是否相同"""
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self,expiration=3600):
        """使用秘钥和时间，为ID生成加密签名，然后对数据和签名进行序列化，生成令牌字符串返回"""
        serializer = Serializer(current_app.config['SECRET_KEY'],expiration)
        return serializer.dumps({'confirm': self.user_id})

    @staticmethod
    def verify_auth_token(token):
        """"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['confirm'])


    @staticmethod
    def confirm(token):
        """激活处理方法"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(data['confirm'])
        print('confirm in user {}'.format('confirm'))
        if not user:  # 用户不存在
            return False

        if not user.confirmed:
            user.confirmed = True
        db.session.add(user)
        db.session.commit()
        return True


    def __repr__(self):
        return '<User {}>'.format(self.username)






if __name__ == "__main__":
    u = User('admin','123','admin@125.com')
    print(u)




