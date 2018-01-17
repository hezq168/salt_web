# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from flask_login import login_required,current_user,login_user,logout_user
from flask import render_template,redirect,url_for,request,flash,session
from . import auth
from .forms import LoginFrom
import sys
from ..models import User,Role
# 引入md5
from hashlib import md5

reload(sys)
sys.setdefaultencoding('utf8')

#用户登录
@auth.route('/login',methods=['GET', 'POST'])
def login():
    form = LoginFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        md5_pw = md5(form.password.data).hexdigest()  #获取用户密码并MD5
        # 判断用户状态 0 未禁用，1 禁用
        if user.status == 0:
            # 判断邮箱和密码
            if user is not None and user.password == md5_pw:
                login_user(user, form.remember_me.data)
                #取出用户数据
                user_obj = Role.query.filter(Role.id == user.id).first()
                #存入session中
                #session['user'] = user_obj
                session['user'] = {'role': {user_obj.id: user_obj.name},
                                   'node': {}}
                #循环把节点权限存入session中
                for node in user_obj.node_id:
                    session['user']['node'][node.id] = node.name
                return redirect(url_for('main.index'))
            else:
                flash('用户名或密码错误！！！')
        else:
            flash('用户被禁用，联系管理员处理！')
    return render_template('auth/login.html', form=form)

#用户退出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('退出成功')
    return redirect(url_for('auth.login'))