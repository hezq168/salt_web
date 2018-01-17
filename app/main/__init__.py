# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from flask import Blueprint
main = Blueprint('main', __name__)

from . import views,user,hosts,errors

