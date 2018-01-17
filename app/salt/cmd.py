# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import render_template, request, jsonify,abort
from flask_login import current_user,login_required
from . import salt
from ..decorators import permission_required
from salt_api import SaltApi
from salt_log import salt_log


@salt.route('/salt_cmd/',methods=['post','get'])
@login_required
@permission_required(22)
def salt_cmd():
    if request.method == 'GET':
        key = SaltApi.Key('key.list_all')
        # 认证的主机列表
        minions = key['return'][0]['data']['return']['minions']
        return render_template('salt/salt_cmd.html',minions=minions)

    if request.method == 'POST' and request.is_xhr:
        host = request.form.get('host')
        cmd = request.form.get('cmd')
        # 异步cmd,返回jid
        ret  = SaltApi.Async(host,cmd)
        try:
            salt_log(ret,host,'cmd.run',cmd)
            return jsonify(ret['return'])
        except:
            return '结果太长！'
    abort(403)
