#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from libs.value_dispatch import value_dispatch
from config.wxmenu import Mainmenu, SitEnvMenu, AsiaMenu
from config.conf import deploy_auth_config
import common.kubesphere as kk


@value_dispatch
def recived_msg(content, fromuser):
    return "输入help查看帮助"


# help菜单
@recived_msg.register_for_all(
    {
        'help',
        ''
    }
)
def send_menu(content, fromuser=None):
    if fromuser in deploy_auth_config['admin']:
        if content == 'help':
            return Mainmenu()
    if fromuser in deploy_auth_config['sit-all']:
        if content == 'help':
            return SitEnvMenu()
    return "联系管理员开通权限！"


# suvery项目
@recived_msg.register_for_all(
    {
        'suprd',
        'sudev'
    }
)
def deploy_suvery(jobname, fromuser=None):
    if fromuser in deploy_auth_config['admin']:
        if jobname == 'suprd':
            kk.buildstandardpipeline('prod', 'asiarnktf', 'survey', 'master', fromuser)
            content = '【Survey--PRD】部署任务已发起，请稍后……'
            return content
    if fromuser in deploy_auth_config['admin'] or fromuser in deploy_auth_config['sit-all']:
        if jobname == 'sudev':
            kk.buildstandardpipeline('dev', 'asialhhf8', 'survey', 'develop', fromuser)
            content = '【Survey--DEV】部署任务已发起，请稍后……'
            return content
    return f'你没有被授权发布【{jobname}】，请联系管理员！'
