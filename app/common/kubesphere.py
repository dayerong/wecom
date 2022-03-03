#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests

from config.conf import kubesphere_config
from common.jnks import insertbuildrecord


def asia_platform_params(subitem):
    data = {
        "parameters": [
            {
                "name": "subobject",
                "value": subitem
            },
            {
                "name": "db_update_flag",
                "value": "True"
            }
        ]
    }
    return data


def get_token(env):
    url = "{url}/oauth/token".format(url=kubesphere_config[env]['url'])
    payload = {
        "grant_type": "password",
        "username": kubesphere_config[env]['username'],
        "password": kubesphere_config[env]['password']
    }

    res = requests.post(url=url, data=payload)
    token = res.json()['access_token']
    return token


def multibranchespipeline(env, token, project, pipeline_name, branch_name, payload=None):
    url = "{url}/kapis/devops.kubesphere.io/v1alpha2/devops/{project}/pipelines/{pipeline_name}/branches/{branch_name}/runs".format(
        url=kubesphere_config[env]['url'],
        project=project,
        pipeline_name=pipeline_name,
        branch_name=branch_name
    )
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {token}'.format(token=token)
    }

    data = json.dumps(payload, ensure_ascii=False)
    res = requests.post(url=url, data=data, headers=headers)
    return res.text


def buildstandardpipeline(env, project, pipeline_name, branch_name, build_user):
    token = get_token(env)
    res = multibranchespipeline(env, token, project, pipeline_name, branch_name)
    buildid = json.loads(res)['id']
    job_name = "{0}/{1}/{2}".format(project, pipeline_name, branch_name)
    rs = insertbuildrecord(buildid, build_user, job_name)
    return rs


def buildparameterspipeline(env, project, pipeline_name, branch_name, params, build_user):
    token = get_token(env)
    res = multibranchespipeline(env, token, project, pipeline_name, branch_name, params)
    buildid = json.loads(res)['id']
    job_name = "{0}/{1}/{2}".format(project, pipeline_name, branch_name)
    rs = insertbuildrecord(buildid, build_user, job_name)
    return rs


def build_asia_pipeline(env, project, pipeline_name, branch_name, subitem, build_user):
    asia_params = asia_platform_params(subitem)
    rs = buildparameterspipeline(env, project, pipeline_name, branch_name, asia_params, build_user)
    return rs
