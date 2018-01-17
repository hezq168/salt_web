# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import render_template, request, jsonify
from flask_login import login_required
from . import main
from app.models import User,Role,Node
from app import db
from datetime import datetime
# 引入md5
from hashlib import md5
import json
from ..decorators import permission_required




@main.route('/user/')
@login_required
@permission_required(1)
def user():
    # 取出所有用户数据
    user = User.query.filter_by().all()
    role = Role.query.filter_by().all()

    return render_template('user/user.html',users=user,roles=role)


# 添加用户
@main.route('/add_user/',methods=['post'])
@login_required
@permission_required(2)
def add_user():
    # 检查是否为ajax请求
    if request.method == 'POST':
        username = request.form.get('add_username', u'无用户名')
        pwd = request.form.get('add_password', u'无密码')
        name = request.form.get('add_name', u'无密码')
        sex = request.form.get('add_sex','')
        qq = request.form.get('add_qq','')
        email = request.form.get('add_email', u'无邮箱')
        tel = request.form.get('add_tel','')
        role_id = request.form.get('add_role','')
        if username and pwd:
            _user = User(username=username, password=md5(pwd).hexdigest(), name=name,email=email, sex=sex, role_id=role_id,
                         tel=tel, qq=qq, login_date=datetime.now())
            db.session.add(_user)
            db.session.commit()
            msg = {'status': 'ok', 'title': '添加用户', 'txt': '添加用户成功' }
            return jsonify(msg)
        else:
            msg = {'status': 'error', 'title': '添加用户', 'txt': '添加用户失败' }
            return jsonify(msg)
    else:
        return '请求不合法！'

# 用户状态修改
@main.route('/user_status/',methods=['get'])
@login_required
@permission_required(3)
def user_status():
    if request.is_xhr:
        uid = request.args.get('user_id')
        ustatus = int(request.args.get('user_op'))
        u = User.query.filter_by(id=uid).first()
        #  ustatus 1 表示禁用，0 表示启动
        if ustatus == 1:
            u.status = 1
            db.session.commit()
            msg = {'status':'ok','title':'禁用用户','txt':'禁用成功'}
            return jsonify(msg)
        else:
            u.status = 0
            db.session.commit()
            msg = {'status':'ok','title':'激活用户','txt':'激活成功'}
            return jsonify(msg)
    else:
        return '数据请求不合法!'

# 修改用户
@main.route('/edit_user/',methods=['get','post'])
@login_required
@permission_required(3)
def edit_user():
    if request.method == 'GET'and request.is_xhr:
        user_id = request.args.get('user_id')
        user = User.query.filter_by(id=user_id).first()
        return jsonify(user.to_json())
    elif request.method == 'POST'and request.is_xhr:
        edit_id = request.form.get('edit_id')
        edit_username = request.form.get('edit_username')
        edit_name = request.form.get('edit_name')
        edit_sex = request.form.get('edit_sex')
        edit_tel = request.form.get('edit_tel')
        edit_qq = request.form.get('edit_qq')
        edit_email = request.form.get('edit_email')
        edit_role = request.form.get('edit_role')
        _update = {"username":edit_username,"name":edit_name,"sex":edit_sex,"tel":edit_tel,"qq":edit_qq,
                   "email":edit_email,"role_id":edit_role}
        User.query.filter_by(id=edit_id).update(_update)
        db.session.commit()
        msg = {'status': 'ok', 'title': '更新用户', 'txt': '更新用户成功' }
        return jsonify(msg)
    else:
        return '请求不合法！'


# 添加用户时检查用户名
@main.route('/check_user/', methods=['get'])
@login_required
def check_user():
    if request.is_xhr:
        username = User.query.filter_by(username=request.args.get('add_username','').lower()).first()
        return jsonify(username is None)
    else:
        return '请求不合法!'

# 添加用户时检查邮箱
@main.route('/check_email/', methods=['get'])
@login_required
def check_email():
    if request.is_xhr:
        email = User.query.filter_by(email=request.args.get('add_email','').lower()).first()
        return jsonify(email is None)
    else:
        return u'请求不合法!'


# 用户角色
@main.route('/role/')
@login_required
@permission_required(5)
def role():
    role = Role.query.filter_by().all()
    node = Node.query.filter_by().all()
    return render_template('user/roles.html', roles=role, nodes=node)


# 添加角色
@main.route('/add_role/',methods=['POST'])
@login_required
@permission_required(6)
def add_role():
    if request.is_xhr and request.method == 'POST':
        name = request.form.get('role')
        add_role_node = request.form.get('add_role_node')
        node = map(int, json.loads(request.form.get('node')))
        if name:
            if node:
                r = Role(name=name, txt=add_role_node)
                for n in node:
                    n = Node.query.filter_by(id=n).first()
                    r.node_id.append(n)
                    db.session.add(r)
                    db.session.commit()
                msg ={'status':'ok','title':'添加角色','txt':'添加角色成功!'}
                return jsonify(msg)
            else:
                msg ={'status':'error','title':'添加角色','txt':'权限不能空!'}
                return jsonify(msg)
        else:
            msg ={'status':'error','title':'添加角色','txt':'角色名不能空!'}
            return jsonify(msg)

    else:
        return '请求数据不合法！'


# 删除角色
@main.route('/del_role/',methods=['POST'])
@login_required
@permission_required(8)
def del_role():
    if request.method == 'POST' and request.is_xhr:
        role_id = request.form.get('role_id')
        if role_id:
            user = User.query.filter_by(role_id=role_id).first()
            if user:
                msg ={'status':'error','title':'删除角色失败','txt':'角色下面有用户，不能删除失败!'}
                return jsonify(msg)
            else:
                r = Role.query.filter_by(id=role_id).first()
                db.session.delete(r)
                db.session.commit()
                msg ={'status':'ok','title':'删除角色成功','txt':'角色删除成功!'}
                return jsonify(msg)
        else:
            return '请求数据不合法!'
    else:
        return '请求数据不合法!'



# 修改角色
@main.route('/edit_role/',methods=['POST','GET'])
@login_required
@permission_required(7)
def edit_role():
    if request.method == 'GET'and request.is_xhr:
        role_id = request.args.get('role_id')
        _role = Role.query.filter_by(id=role_id).first()
        node_id = []
        for n in _role.node_id:
            node_id.append(n.id)
        role_json = {'role_id':_role.id,'role_name':_role.name,'role_txt':_role.txt,'node_id':node_id}
        return jsonify(role_json)

    elif request.method == 'POST' and request.is_xhr:
        role_id = request.form.get('role_id')
        name = request.form.get('role_name')
        role_txt = request.form.get('role_txt')
        node = map(int, json.loads(request.form.get('node_id')))

        if name:
            if node:
                r = Role.query.filter_by(id=role_id).first()
                r.name = name
                r.txt = role_txt
                del r.node_id[:]
                for n in node:
                    n = Node.query.filter_by(id=n).first()
                    r.node_id.append(n)
                    db.session.add(r)
                    db.session.commit()
                msg ={'status':'ok','title':'更新角色','txt':'更新角色成功!'}
                return jsonify(msg)
            else:
                msg ={'status':'error','title':'更新角色','txt':'权限不能空!'}
                return jsonify(msg)
        else:
            msg ={'status':'error','title':'更新角色','txt':'角色名不能空!'}
            return jsonify(msg)