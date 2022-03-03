#!/usr/bin/env python
# -*- coding: utf-8 -*-

import jenkins
from config.conf import jenkins_config, infratools_config
import requests
import json
import urllib3

urllib3.disable_warnings()


def insertbuildrecord(build_id, build_user, project_name):
    url = infratools_config['jenkins_jobs_api_url']
    data = {
        "project_name": project_name,
        "build_id": build_id,
        "build_user": build_user
    }
    data = json.dumps(data, ensure_ascii=False)
    r = requests.post(url=url, data=data.encode('utf-8'))
    return r.text


class JenkinsOperation(object):
    def __init__(self):
        self.jenkins_url = jenkins_config['jenkins_url']
        self.user = jenkins_config['user']
        self.password = jenkins_config['password']

    def buildjob(self, job_name, param=None, build_user=None):
        op = jenkins.Jenkins(self.jenkins_url, self.user, self.password)
        last_build_number = op.get_job_info(job_name)['lastCompletedBuild']['number']
        build_number = last_build_number + 1
        rs = insertbuildrecord(build_number, build_user, job_name)
        op.build_job(job_name, param)
        return rs

    def getjobs(self):
        op = jenkins.Jenkins(self.jenkins_url, self.user, self.password)
        jobs = op.get_jobs()
        print(jobs)
