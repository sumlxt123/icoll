#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


"""
完成用户注册、登录、验证、完善信息、修改信息、修改密码等功能
"""


from flask import url_for,request,current_app
from flask import Blueprint,render_template,redirect,flash
from flask_login import login_user,logout_user,login_required,LoginManager
from .forms import LoginForm,RegisterForm
from ..models import db,User
from ..email import send_mail



auth = Blueprint('auth', __name__, template_folder='templates')
login_manager = LoginManager()




@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))



@auth.route('/login', methods=['GET', 'POST'])
def login():
    """登录视图"""
    form = LoginForm()
    if form.validate_on_submit() and request.method=='POST':
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):  # 校验用户密码
            login_user(user)
            return redirect(url_for('auth.user_info'))
        else:
            flash('用户名或密码错误')
            current_app.logger.info('user {0} login flase, please look password is error.'.format(
                form.username.data))
    return render_template('auth/login1.html', form=form)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """注册视图"""
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                        password=form.password.data,
                        email=form.email.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()  # 生产用于激活校验的 token
        send_mail(to=user.email,
                  subject='【icoll账户激活】', template='mail/confirm',
                  user=user, token=token)  # 发送邮件
        flash('注册成功,请登录邮箱点击激活账户')  # 提示用户下一步操作
        return redirect(url_for('main.index'))  # 当用户注册成功，页面自动跳转到用户的索引页面
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    """登出视图"""
    logout_user()
    flash(u'你已退出登录')
    return redirect(url_for('auth.login'))


@auth.route('/user_info')
@login_required
def user_info():
    """用户实例视图，需要登录后访问"""
    return render_template('auth/user.html')


@auth.route('/confirm/<token>')
def confirm(token):
    """激活账户应该先与用户登录"""
    if User.confirm(token):
        # 激活成功
        flash('激活成功，请登录')
        redirect(url_for('auth.login'))
    else:
        flash('账号未激活，请激活！！！')
    return redirect(url_for('main.index'))


@auth.route('/unconfirmed')
def unconfirmed():
    """如果当前账号是匿名账号或已经确认，直接返回首页，否则显示为未确认"""
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.idex'))
    return render_template('auth/unconfirmed.html')


@auth.route('/resend_email')
@login_required
def resend_email():
    token = current_user.generate_confirmation_token()
    send_mail(current_user.email, u'账号确认', 'mail/confirm',
              user=current_user, token=token)
    flash(u'一份新的激活邮件已发完你的邮箱，请前往激活，邮件1个小时内有效')
    return redirect(url_for('main.index'))


@auth.route('/send_email')
def send_email():
    """测试邮件发送是否正常"""
    send_mail(to='sunlxt123@163.com',
              subject='【测试icoll账户激活】', template='mail/test',username='测试用户')  # 发送邮件
    return '<h1>邮件发送成功</h1>'
