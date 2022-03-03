#!/usr/bin/env python
# -*- encoding: utf-8 -*-


# 日志配置
log_config = {
    "logformat": "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    "loglevel": 20,  # 0 NOSET, 10 DEBUG, 20 INFO, 30 WARNING, 40 ERROR, 50 CRITICAL
    "file": "./app/logs/app.log",
    "datefmt": "%Y/%m/%d %H:%M:%S",
    "ssh_log_file": "./app/logs/ssh.log"
}

# 企业微信应用网页授权、接收消息API信息
insvc_wxauth_config = {
    "Corpid": "",
    "Secret": "",
    "Agentid": "",
    "Token": "",
    "EncodingAESKey": ""
}

# Jenkins信息
jenkins_config = {
    "jenkins_url": "http://10.0.1.11:8080/",
    "user": "devops",
    "password": "devops@jkns"
}

# 部署人员权限
deploy_auth_config = {
    "new-retail-prd": ['8333', '8298'],
    "new-retail-dev": ['8333', '8298'],
    "dms-prd": ['8333', '8298'],
    "dms-dev": ['8333', '8731', '8690'],
    "admin": ['8333'],
    "sit-all": ['8560', '8946']
}

# infra-tools API
infratools_config = {
    "jenkins_jobs_api_url": "http://infra-api.xxx.com/CICD/v1/build",
}

# kubesphere API
kubesphere_config = {
    "dev": {"url": "http://10.0.3.60:31158",
            "username": "devops",
            "password": "devops@dev"
            },
    "prod": {"url": "http://10.0.1.71:31152",
             "username": "devops",
             "password": "devops@prd"
             }
}
