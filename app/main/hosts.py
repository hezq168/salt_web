# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import render_template, request, jsonify
from flask_login import login_required
from . import main
from app import db
from ..decorators import permission_required
from app.models import Hosts,HostsGroup,User


# 主机
@main.route('/hosts/')
@login_required
@permission_required(10)
def hosts():
    host = Hosts.query.filter_by().all()
    group = HostsGroup.query.filter_by().all()
    user = User.query.filter_by().all()
    return render_template('hosts/hosts.html', host=host,groups=group,users=user)


# 主机ip址检查
@main.route('/check_host_ip/',methods=['GET'])
@login_required
def check_host_ip():
    if request.is_xhr:
        host_group = Hosts.query.filter_by(ip=request.args.get('add_ip','').lower()).first()
        return jsonify(host_group is None)
    else:
        return '请求不合法!'

# 添加主机
@main.route('/add_hosts/',methods=['POST'])
@login_required
@permission_required(11)
def add_hosts():
    if request.is_xhr:
        ip = request.form.get('add_ip')
        name = request.form.get('add_host_name')
        mini = request.form.get('add_mini',None)
        isp = request.form.get('add_isp')
        type = request.form.get('add_type')
        zone = request.form.get('add_zone')
        server = request.form.get('add_server')
        user = request.form.get('add_user')
        group = request.form.get('add_group')
        if not ip:
            return '数据不完整，无法请求！'
        else:
            _ip = Hosts.query.filter_by(ip=ip).first()
            if _ip:
                return '主机已存在！'
            else:
                host = Hosts(ip=ip,name=name,minion=mini,isp=isp,type=type,zone=zone,server=server,user=user,group_id=group)
                try:
                    db.session.add(host)
                    db.session.commit()
                    msg = {'status': 'ok', 'title': '添加主机', 'txt': '添加主机成功' }
                    return jsonify(msg)
                except:
                    msg = {'status': 'error', 'title': '添加主机', 'txt': '添加主机失败' }
                    return jsonify(msg)
    else:
        return '请求不合法！'


# 修改主机
@main.route('/edit_hosts/',methods=['POST','GET'])
@login_required
@permission_required(12)
def edit_hosts():
    if request.method=='GET' and request.is_xhr:
        host_id = request.args.get('host_id')
        if host_id:
            host = Hosts.query.filter_by(id=host_id).first()
            return jsonify(Hosts.to_json(host))
        else:
            return '数据请求不合法!'
    if request.method=='POST' and request.is_xhr:
        id = request.form.get('edit_id')
        if id:
            ip = request.form.get('edit_ip')
            name = request.form.get('edit_host_name')
            minion = request.form.get('edit_mini',None)
            isp = request.form.get('edit_isp')
            type = request.form.get('edit_type')
            zone = request.form.get('edit_zone')
            server = request.form.get('edit_server')
            user = request.form.get('edit_user')
            group_id = request.form.get('edit_group')
            _update = {"ip":ip,"name":name,"minion":minion,"isp":isp,"type":type,"zone":zone,"server":server,"user":user,
                       "group_id":group_id}
            Hosts.query.filter_by(id=id).update(_update)
            db.session.commit()
            msg = {'status': 'ok', 'title': '更新主机', 'txt': '更新主机成功' }
            return jsonify(msg)
        else:
            msg = {'status': 'error', 'title': '更新主机', 'txt': '更新主机失败' }
            return jsonify(msg)

    return '数据不合法！'
# 删除主机
@main.route('/del_hosts/', methods=['POST'])
@login_required
@permission_required(13)
def del_hosts():
    if request.method =='POST' and request.is_xhr:
        host_id = request.form.get('host_id')
        if host_id:
            host = Hosts.query.filter_by(id=host_id).first()
            try:
                db.session.delete(host)
                db.session.commit()
                msg = {'status': 'ok', 'title': '删除主机', 'txt': '删除主机组成功' }
                return jsonify(msg)
            except:
                msg = {'status': 'error', 'title': '删除主机', 'txt': '删除主机组失败' }
                return jsonify(msg)
        else:
            return '数据不合法！'
    else:
        return '数据不合法!'






# 主机组
@main.route('/hosts_group/')
@login_required
@permission_required(14)
def hosts_group():
    group = HostsGroup.query.filter_by().all()

    return render_template('hosts/hosts_group.html', groups=group)

# 添加主机组
@main.route('/add_hosts_group/', methods=['POST'])
@login_required
@permission_required(15)
def add_hosts_group():
    if request.method == 'POST' and request.is_xhr:
        host_group = request.form.get('host_group')
        host_group_txt = request.form.get('host_group_txt')
        if host_group:
            group = HostsGroup(name=host_group,txt=host_group_txt)
            db.session.add(group)
            db.session.commit()
            msg = {'status': 'ok', 'title': '添加主机组', 'txt': '添加主机组成功' }
            return jsonify(msg)
        else:
            msg = {'status': 'error', 'title': '添加主机组', 'txt': '添加主机组失败' }
            return jsonify(msg)

# 修改主机组
@main.route('/edit_hosts_group/',methods=['GET','POST'])
@login_required
@permission_required(16)
def edit_hosts_group():
    if request.method =='GET' and request.is_xhr:
        group_id = request.args.get('group_id')
        group = HostsGroup.query.filter_by(id=group_id).first()
        _group = {'id':group.id,'name':group.name,'txt':group.txt}
        return jsonify(_group)
    elif request.method == 'POST' and request.is_xhr:
        group_id = request.form.get('group_id')
        name = request.form.get('edit_group')
        txt = request.form.get('edit_group_txt')
        group = HostsGroup.query.filter_by(id=group_id).first()
        try:
            group.name = name
            group.txt = txt
            db.session.commit()
            msg = {'status': 'ok', 'title': '修改主机组', 'txt': '修改主机组成功' }
            return jsonify(msg)
        except:
            msg = {'status': 'error', 'title': '修改主机组', 'txt': '修改主机组失败' }
            return jsonify(msg)
    else:
        return '请求不合法！'

# 检查主机组是否重复
@main.route('/check_host_group/',methods=['get'])
@login_required
def check_host_group():
    if request.is_xhr:
        host_group = HostsGroup.query.filter_by(name=request.args.get('host_group','').lower()).first()
        return jsonify(host_group is None)
    else:
        return '请求不合法!'

# 删除主机组
@main.route('/del_hosts_group/',methods=['POST'])
@login_required
@permission_required(17)
def del_hosts_group():
    if request.is_xhr:
        group_id = request.form.get('group_id')
        if group_id:
            hosts = Hosts.query.filter_by(group_id=group_id).first()
            if hosts:
                msg = {'status': 'error', 'title': '删除主机组', 'txt': '删除主机组失败，组下面有主机！'}
                return jsonify(msg)
            else:
                hosts_group = HostsGroup.query.filter_by(id=group_id).first()
                db.session.delete(hosts_group)
                db.session.commit()
                msg = {'status': 'ok', 'title': '删除主机组', 'txt': '删除主机组成功！'}
                return jsonify(msg)
        else:
            return '请求不合法'
    else:
        return '请求不合法'