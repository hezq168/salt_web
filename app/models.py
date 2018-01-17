# -*- coding:utf-8 -*-
__author__ = 'Administrator'
from . import login_manager, db
from flask_login import UserMixin,AnonymousUserMixin,current_user
from flask import session


# 角色-节点关系表
role_node = db.Table('role_node',
                     db.Column('id',db.Integer,primary_key=True),
                     db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                     db.Column('node_id', db.Integer, db.ForeignKey('node.id'))
                     )

#用户表
class User(UserMixin,db.Model):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))   # 用户名
    password = db.Column(db.String(64))   # 密码
    name = db.Column(db.String(32))       # 姓名
    login_date = db.Column(db.DateTime())  # 最后一次登录日期
    sex = db.Column(db.String(64))
    qq = db.Column(db.String(64))
    email = db.Column(db.String(64))
    tel = db.Column(db.String(255))
    avatar =db.Column(db.String(64),default='2e290c00150943b02940a0f680ca67aa.png')  # 头像文件
    status = db.Column(db.Integer,default=0)      #用户状态 0:激活  1:禁用
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))  #  角色外键

    def __repr__(self):
        return '<username %r>' % (self.username)

    def to_json(self):
        return dict(id=self.id,username=self.username,sex=self.sex,name=self.name,qq=self.qq,
                    email=self.email,tel=self.tel,role_id=self.role_id)

    def can(self,permissions):
        if permissions:
            if self.role_id == 1:
                return True
            if session['user']['node']. has_key(permissions):
                return True
            return False
        return False

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False


login_manager.anonymous_user = AnonymousUser

# 角色表
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))   # 角色名
    txt = db.Column(db.String(64))    # 角色说明
    users = db.relationship('User', backref='role')
    node_id = db.relationship('Node', secondary=role_node, backref='role_node')

    def __repr__(self):
        return '<Role %r>' % self.name


# 节点表
class Node(db.Model):
    __tablename__ ='node'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))   # 节点名
    txt = db.Column(db.String(64))    # 节点说明

    def __repr__(self):
        return '<node %r>' % self.id


# 主机表
class Hosts(db.Model):
    __tablename__ = 'hosts'
    id = db.Column(db.Integer,primary_key=True)
    ip = db.Column(db.String(32))      # ip 地址
    name = db.Column(db.String(32))  # 主机名
    isp = db.Column(db.String(32))   # 运营商
    minion = db.Column(db.String(32))  # Minionid
    type = db.Column(db.String(32))  # 类别
    zone = db.Column(db.String(32))   # 地区
    user = db.Column(db.String(32))  # 维护人员
    server = db.Column(db.String(32))  # 机房
    group_id = db.Column(db.Integer, db.ForeignKey('hosts_group.id'))  #  主机组外键

    def to_json(self):
        return dict(id=self.id,ip=self.ip,name=self.name,isp=self.isp,minion=self.minion,type=self.type,zone=self.zone,
                    user=self.user,server=self.server,group_id=self.group_id)

# 主机组
class HostsGroup(db.Model):
    __tablename__ = 'hosts_group'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(32))
    txt = db.Column(db.String(32))
    host = db.relationship('Hosts', backref='hosts_group')



# salt_log
class SaltLog(db.Model):
    __tablename__ = 'salt_log'
    id = db.Column(db.Integer,primary_key=True)
    user = db.Column(db.String(32))
    log = db.Column(db.String(1000))
    jid = db.Column(db.String(64))
    target = db.Column(db.String(32))
    date = db.Column(db.DATETIME)
    type = db.Column(db.String(16))  # 日志类型
    cmd = db.Column(db.String(32))  # 命令



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))