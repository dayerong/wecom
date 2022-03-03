#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import time
import xml.etree.cElementTree as ET
from fastapi import APIRouter, Depends
from config.conf import insvc_wxauth_config
from libs.WXBizMsgCrypt import WXBizMsgCrypt
from libs.WXXmlBody import XmlBody
from common.logs import Log
from model.wxmodels import Item
from common.recivetext import recived_msg
from common.reciveevent import recived_event


def wxmsgcpt():
    sCorpID = insvc_wxauth_config["Corpid"]
    sEncodingAESKey = insvc_wxauth_config["EncodingAESKey"]
    sToken = insvc_wxauth_config["Token"]
    wxcpt = WXBizMsgCrypt(sToken, sEncodingAESKey, sCorpID)
    return wxcpt


router = APIRouter()
wxcpt = wxmsgcpt()


# 回调验证部分
@router.get("/itsvc")
async def Verify(msg_signature: str,
                 timestamp: str,
                 nonce: str,
                 echostr: str
                 ):
    sVerifyMsgSig = msg_signature
    sVerifyTimeStamp = timestamp
    sVerifyNonce = nonce
    sVerifyEchoStr = echostr
    ret, sReplyEchoStr = wxcpt.VerifyURL(sVerifyMsgSig, sVerifyTimeStamp, sVerifyNonce, sVerifyEchoStr)
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)
    return int(sReplyEchoStr)


# 接受消息模版
Recived_Temp = """
<xml> 
   <ToUserName><![CDATA[%(ToUserName)s]]></ToUserName>
   <AgentID><![CDATA[%(AgentID)s]]></AgentID>
   <Encrypt><![CDATA[%(Encrypt)s]]></Encrypt>
</xml>
"""

# 发送消息模版
Send_Temp = """
<xml>
   <ToUserName>%(ToUserName)s</ToUserName>
   <FromUserName>%(FromUserName)s</FromUserName> 
   <CreateTime>%(timestamp)s</CreateTime>
   <MsgType>text</MsgType>
   <Content>%(content)s</Content>
</xml>
"""


# 消息接收部分
@router.post("/itsvc")
async def sendMsg(msg_signature: str,
                  timestamp: str,
                  nonce: str,
                  item: Item = Depends(XmlBody(Item))
                  ):
    Recived_dict = {
        'ToUserName': item.ToUserName,
        'AgentID': item.AgentID,
        'Encrypt': item.Encrypt,
    }

    ReqData = Recived_Temp % Recived_dict
    ret, sMsg = wxcpt.DecryptMsg(sPostData=ReqData, sMsgSignature=msg_signature, sTimeStamp=timestamp, sNonce=nonce)
    if (ret != 0):
        print("ERR: DecryptMsg ret: " + str(ret))
        sys.exit(1)
    xml_tree = ET.fromstring(sMsg)
    FromUserName = xml_tree.find("FromUserName").text
    ToUserName = xml_tree.find("ToUserName").text
    msgType = xml_tree.find("MsgType").text

    def SendTextMsg(ToUserName, FromUserName, content):
        timestamp = str(time.time())
        Send_dict = {
            "ToUserName": ToUserName,
            "FromUserName": FromUserName,
            "timestamp": timestamp,
            "content": content,
        }
        # 消息发送部分
        sRespData = Send_Temp % Send_dict
        ret, sEncryptMsg = wxcpt.EncryptMsg(sReplyMsg=sRespData, sNonce=nonce, timestamp=timestamp)
        if (ret != 0):
            print("ERR: EncryptMsg ret: " + str(ret))
            sys.exit(1)
        return sEncryptMsg

    if msgType == 'text':
        logger = Log()
        content_recived = xml_tree.find("Content").text
        # 接收消息执行命令
        content = recived_msg(content_recived.lower(), fromuser=FromUserName)
        contentlog = "WeComAPI Service : [%s to %s][%s]" % (FromUserName, ToUserName, content)
        logger.info(f'[text][{content_recived}]', contentlog)
        sEncryptMsg = SendTextMsg(ToUserName, FromUserName, content)
        return sEncryptMsg

    if msgType == 'event':
        logger = Log()
        try:
            event = xml_tree.find("Event").text
            eventKey = xml_tree.find("EventKey").text
            if event == 'click':
                content = recived_event(eventKey, fromuser=FromUserName)
                contentlog = "WeComAPI Service : [%s to %s][%s]" % (FromUserName, ToUserName, content)
                logger.info(f'[event][{eventKey}]', contentlog)
                sEncryptMsg = SendTextMsg(ToUserName, FromUserName, content)
                return sEncryptMsg
        except AttributeError:
            pass
        except Exception as err:
            logger.error(f'[event]', err)
            print(err)
