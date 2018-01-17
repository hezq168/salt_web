# -*- coding:utf-8 -*-
import urllib2
import json
from config import Config

class SaltAPI(object):
    __token_id = ''
    def __init__(self,url,username,password):
        self.__url = url.rstrip('/')
        self.__user = username
        self.__password = password
    # 获取token_id
    def token_id(self):
        headers ={"Content-type":"application/x-yaml","Accept": "application/json"}
        params = json.dumps({"eauth":"pam","username":self.__user,"password":self.__password})
        req = urllib2.Request(self.__url+'/login',params,headers)
        respones = urllib2.urlopen(req)
        try:
            result = json.loads(respones.read())
            # 获取salt token
            self.__token_id = result['return'][0]['token']
        except KeyError:
            raise KeyError
    # 获取数据
    def postRequest(self,body=None,prefix='/'):
        url = self.__url + prefix
        headers = {"Content-type": "application/json","Accept": "application/json", "X-Auth-Token": self.__token_id}
        req = urllib2.Request(url, body, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content

    # key模块
    def Key(self,fun,node_name=None):
        body = json.dumps({
            "client": "wheel",
            "fun": fun,
            "match": node_name,  # 节点
        })
        self.token_id()
        req = self.postRequest(body)
        return req

    # cmd.run模块
    def Cmd(self,tgt, arg):
        body = json.dumps({
            "client": "local",
            "fun": "cmd.run",      # fun 就是模块的名字和方法名字
            "tgt": tgt,            # tgt 目标
            "arg": arg,            # arg 命令
        })
        self.token_id()
        req = self.postRequest(body)
        return req

    # 异步模块
    def Async(self,tgt, arg):
        body = json.dumps({
            "client": "local_async",  # 异步
            "fun": "cmd.run",      # fun 就是模块的名字和方法名字
            "tgt": tgt,            # tgt 目标
            "arg": arg,            # arg 命令
        })
        self.token_id()
        req = self.postRequest(body)
        jid = req['return'][0]['jid']
        return self.Jobs(jid)

    def Jobs(self,jid=None):
        self.token_id()
        if jid is None:
            req = self.postRequest(prefix='/jobs')
        else:
            req = self.postRequest(prefix='/jobs/'+jid)
        return req


config = Config()
SaltApi = SaltAPI(url=Config.SaltApi_URL, username=Config.SaltApi_USERNAME, password=Config.SaltApi_PASSWORD)