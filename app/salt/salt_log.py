# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask_login import current_user
from app import db
from app.models import SaltLog
from datetime import datetime


# results返回结果
# target操作范围
# op动作类型
# cmd命令
def salt_log(results,target,op=None,cmd=None):
    if op == 'key':
        jid = results['return'][0]['data']['jid']
        re = SaltLog(user=current_user.name,log=str(results),target=target,date=datetime.now(),jid=jid,type=op,cmd=cmd)
        db.session.add(re)
    # cmd异步
    elif op == 'cmd.run':
        jid = results['info'][0]['jid']
        re = SaltLog(user=current_user.name,log=str(results),target=target,date=datetime.now(),jid=jid,type=op,cmd=cmd)
        db.session.add(re)
    else:
        return '命令不合法!'

    db.session.commit()