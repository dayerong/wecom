#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from libs.value_dispatch import value_dispatch
from config.conf import deploy_auth_config
from common.jnks import JenkinsOperation


@value_dispatch
def recived_event(eventkey, fromuser):
    return "联系管理员开通权限！"


@recived_event.register_for_all(
    {
        'retail_prd_deploy',
        'retail_h5_prd_deploy',
        'retail_h5_dev_deploy'
    }
)
def deploy_retail(eventkey, fromuser=None):
    if fromuser in deploy_auth_config['new-retail-prd']:
        # 新零售生产环境PC端
        if eventkey == 'retail_prd_deploy':
            op = JenkinsOperation()
            op.buildjob("Mall-PRD", {"Choice": "Deploy"}, build_user=fromuser)
            content = '【Mall-PRD】部署任务已发起，请稍后……'
            return content

        # 新零售生产环境H5端
        if eventkey == 'retail_h5_prd_deploy':
            op = JenkinsOperation()
            op.buildjob("mall-h5/master", {"Choice": "Deploy"}, build_user=fromuser)
            content = '【mall-h5/master】部署任务已发起，请稍后……'
            return content
    if fromuser in deploy_auth_config['new-retail-prd'] or fromuser in deploy_auth_config['new-retail-dev']:
        # 新零售测试环境H5端
        if eventkey == 'retail_h5_dev_deploy':
            op = JenkinsOperation()
            op.buildjob("mall-h5/develop", {"Choice": "Deploy"}, build_user=fromuser)
            content = '【mall-h5/develop】部署任务已发起，请稍后……'
            return content
    return '你没有被授权发布此环境，请联系管理员！'
