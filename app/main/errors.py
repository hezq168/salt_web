# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from flask import render_template
from . import main

@main.app_errorhandler(404)
def page_not_found(e):
    return render_template('error/404.html'), 404


@main.app_errorhandler(403)
def page_not_found(e):
    return render_template('error/403.html'), 403