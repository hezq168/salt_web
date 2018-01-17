# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from functools import wraps
from flask import abort
from flask_login import current_user


#model返回，如果Ture表示有权限，False表示无权限
def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator