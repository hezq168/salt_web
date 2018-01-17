#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/16 15:02
# @Author  : Hezq
# @Contact : Hezq168@gmail.com
# @File    : job.py
# @Project : web
# @Software: PyCharm

from flask import render_template, request, jsonify,abort
from flask_login import current_user,login_required
from . import salt
from ..decorators import permission_required
from app.models import SaltLog
from salt_api import SaltApi
from datetime import datetime
from salt_log import salt_log

# 获取所有job
@salt.route('/salt_jobs/', methods=['GET'])
@salt.route('/salt_jobs/<jib>', methods=['GET'])
def salt_jobs(jib=None):
    if jib:
        job = SaltApi.Jobs(jib)
    else:
        job = SaltApi.Jobs()
        items = job['return'][0]
        #
        job = sorted(items.iteritems(), key=lambda d:d[0], reverse = True)
        return render_template('salt/salt_job.html', jobs=job)
    abort(403)