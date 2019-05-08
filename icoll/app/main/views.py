#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

from flask import request,current_app
from flask import render_template,redirect,Blueprint,url_for
from flask_login import login_required


main = Blueprint('main', __name__, template_folder='templates')


@main.route('/')
@login_required
def index():
    return render_template('main/index.html')
