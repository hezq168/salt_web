# -*- coding:utf-8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
    DEBUG = True
    SESSION_TYPE = 'filesystem'
    CSRF_ENABLED = True
    SECRET_KEY = 'f29!7a57a5a74*38123123123801fc31*'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
#   mysql自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False
#   mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://xxxx:@127.0.0.1/xxxx?charset=utf8'
#   打印sql
    SQLALCHEMY_ECHO = True


#   salt-api配置
    SaltApi_URL = 'http://192.168.11.244:8000'
    SaltApi_USERNAME = 'xxxx'
    SaltApi_PASSWORD = 'xxxx'



#   文章分页数
    POSTS_PER_PAGE = 15



    @staticmethod
    def init_app(app):
        pass
