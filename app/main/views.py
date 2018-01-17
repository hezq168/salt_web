# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from datetime import datetime
import sys
from flask import render_template,request,flash,redirect,url_for, current_app, jsonify,session
from flask_login import login_required, current_user
from . import main


@main.route('/')
@login_required
def index():
    return render_template('main/index.html')
