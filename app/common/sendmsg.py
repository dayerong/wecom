#!/usr/bin/env python
# -*- encoding: utf-8 -*-


import requests
import json
import urllib3
from config.conf import insvc_wxauth_config

urllib3.disable_warnings()


def GetToken(Corpid, Secret):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    Data = {
        "corpid": Corpid,
        "corpsecret": Secret
    }
    r = requests.get(url=Url, params=Data, verify=False)
    Token = r.json()['access_token']
    return Token


def SendMessage(Token, User, Agentid, Subject, Content):
    Url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % Token
    Data = {
        "touser": User,
        "msgtype": "text",
        "agentid": Agentid,
        "text": {
            "content": Subject + '\n' + Content
        },
        "safe": "0"
    }
    data = json.dumps(Data, ensure_ascii=False)
    r = requests.post(url=Url, data=data.encode('utf-8'))
    return r.json()


def main(User, Subject, Content):
    Corpid = insvc_wxauth_config["Corpid"]
    Secret = insvc_wxauth_config["Secret"]
    Agentid = insvc_wxauth_config["Agentid"]
    Token = GetToken(Corpid, Secret)
    SendMessage(Token, User, Agentid, Subject, Content)
