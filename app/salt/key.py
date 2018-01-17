# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import render_template, request, jsonify,abort,current_app
from flask_login import login_required
from . import salt
from app import db
from ..decorators import permission_required
from app.models import Hosts,SaltLog
from salt_api import SaltApi
from salt_log import salt_log



# 获取所有salt-mini
@salt.route('/salt_key/')
@login_required
@permission_required(19)
def salt_key():
    key = SaltApi.Key('key.list_all')
    # 认证的主机列表
    minions = key['return'][0]['data']['return']['minions']
    # 未认证的主机列表
    minions_pre = key['return'][0]['data']['return']['minions_pre']
    # 的主机列表
    minions_denied = key['return'][0]['data']['return']['minions_denied']
    # 未认证的主机列表
    minions_rejected = key['return'][0]['data']['return']['minions_rejected']
    keys = {'minions': minions,'minions_pre':minions_pre,'minions_rejected':minions_rejected,'minions_denied':minions_denied}
    #取出所有主机
    hosts = Hosts.query.filter_by().all()
    return render_template('salt/salt_key.html',keys=keys,hosts=hosts)

# 拒绝salt-mini
@salt.route('/del_key/', methods=['post'])
@login_required
@permission_required(21)
def del_key():
    if request.method == 'POST' and request.is_xhr:
        minion = request.form.get('Minion_ID')
        if minion:
            results = SaltApi.Key('key.delete', minion)
            salt_log(results, minion, 'key','key.delete')
            if results['return'][0]['data']['success']:
                msg = {'status': 'ok', 'title': '拒绝Minion ID', 'txt': '拒绝'+ minion +'成功'}
                return jsonify(msg)
            else:
                msg = {'status': 'error', 'title': '拒绝Minion ID', 'txt': '拒绝'+ minion +'失败'}
                return jsonify(msg)
        else:
            return 'minionid不允许为空!'
    else:
        abort(403)

# 允许salt-mini
@salt.route('/add_key/', methods=['post'])
@login_required
@permission_required(20)
def add_key():
    if request.method == 'POST' and request.is_xhr:
        minion = request.form.get('Minion_ID')
        if minion:
            results = SaltApi.Key('key.accept', minion)
            salt_log(results, minion, 'key','key.accept')
            if results['return'][0]['data']['success']:
                msg = {'status': 'ok', 'title': '添加Minion ID', 'txt': '添加'+ minion +'成功'}
                return jsonify(msg)
            else:
                msg = {'status': 'error', 'title': '添加Minion ID', 'txt': '添加'+ minion +'失败'}
                return jsonify(msg)
        else:
            return 'minionid不允许为空!'
    else:
        abort(403)

# 获取所有salt_log
@salt.route('/salt_log/',methods=['GET','POST'])
@login_required
@permission_required(23)
def Salt_log():
    if request.method == 'GET':
        #获取分页数
        page = request.args.get('page',1,type=int)
        #分页
        per_page = current_app.config['POSTS_PER_PAGE']
        log = SaltLog.query.filter().order_by(db.desc(SaltLog.id)).paginate(page,per_page=per_page,error_out=False)
        return render_template('salt/salt_log.html', logs=log)
    elif request.method == 'POST' and request.is_xhr:
        jid = request.form.get('jid')
        ret = SaltLog.query.filter_by(jid=jid).first()
        # 转换为字典
        ret_dict = eval(ret.log)
        try:
            return jsonify(ret_dict['info'][0])
        except:
            return jsonify(ret_dict['return'][0])

    else:
        abort(403)