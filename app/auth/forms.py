# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField
from wtforms.validators import Required,Length


# 用户登录from
class LoginFrom(FlaskForm):
    username = StringField('用户名：', validators=[Required(),Length(1,8,message=u"用户名长度不正确")],render_kw={"placeholder": "用户名",})
    password = PasswordField('密码：', validators=[Required()],render_kw={"placeholder": "密码",})
    remember_me = BooleanField("自动登录", default=False)
    submit = SubmitField('登录')