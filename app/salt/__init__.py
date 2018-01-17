# -*- coding:utf-8 -*-
__author__ = 'Administrator'

from flask import Blueprint
salt = Blueprint('salt', __name__)

from . import key,cmd,job

