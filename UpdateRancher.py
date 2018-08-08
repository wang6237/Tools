#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import time
import fire

rancher_server_url = 'http://xx.xxx.xxx.xx/v2-beta/projects'
access_key = 'xxxxxxxxxxxxxxxx'
secret_key = 'xxxxxxxxxxxxxxxxxxxxxx'


class RancherAPI(object):
    def __init__(self):
        self.access_key = access_key
        self.secret_key = secret_key

    def _get(self, url):
        """
        定义get方法，获取数据
        :param url:
        :return:
        """
        try:
            r = requests.get(url, auth=(self.access_key, self.secret_key))
        except:
            return "error"
        # r.raise_for_status()
        else:
            return r

    def _post(self, url, data=""):
        """
        定义访问Racher的POST方法
        :param url: 因为是要提交数据，所以一般情况为action url
        :param data: 需要提交的数据，需要时json格式的
        :return:
        """
        headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}
        try:
            if data:
                r = requests.post(url, data=json.dumps(data), auth=(self.access_key, self.secret_key), headers=headers)
            else:
                r = requests.post(url, data="", auth=(self.access_key, self.secret_key), headers=headers)
        except:
            return "error"
        else:

            return r

    def query_service(self, project_id, service_id):
        service_url = rancher_server_url + '/%s/service/%s' % (project_id, service_id)
        r = self._get(service_url)
        return r.json()

    def action(self, url, data=""):
        r = self._post(url, data=data)
        return r.json()

class updateService(object):
    def __init__(self):
        pass
    def update(self,imageUuid, project_id, service_id):
        """接收，service upgraded的url、imageUuid、environment、service state，
        根据url获取到，service的url，=> service state =>
        """
        action_url = rancher_server_url + '/' +project_id + '/services/' + service_id + '/?action'
        upgrade_strategy = json.loads(
            '{"inServiceStrategy": {"batchSize": 1,"intervalMillis": 10000,"startFirst": true,"launchConfig": {},"secondaryLaunchConfigs": []}}')

        # action_list = action_url.split('/')

        # project_id = action_list[5]
        # service_id = action_list[7]
        r = RancherAPI()
        service_info = r.query_service(project_id, service_id)
        if service_info['state'] == "upgraded":
            post_data = {
                "rollingRestartStrategy": {
                    "batchSize": 1,
                    "intervalMillis": 2000
                }}


            r.action( action_url + '=finishupgrade', data=post_data)
            time.sleep(5)

        service_info['launchConfig']['imageUuid'] = 'docker:' + imageUuid
        upgrade_strategy['inServiceStrategy']['launchConfig'] = service_info['launchConfig']
        # 执行升级
        action_result = r.action(action_url + '=upgrade', upgrade_strategy)

        # 再次查询service ，查询其状态
        service_info = r.query_service(project_id, service_id)
        sleep_count = 0
        timeout = 60
        while service_info['state'] != "upgraded" and sleep_count < timeout:
            # print "Waiting for upgrade to finish..."
            time.sleep(2)
            service_info = r.query_service(project_id, service_id)
            print(sleep_count, service_info['state'])
            sleep_count += 1

        if service_info['state'] == 'upgraded':
            # 升级成功，返回1
            return json.dumps({'msg': "Update Service Succeed"})
        else:
            # 失败返回0
            return json.dumps({'msg': "Update Service Failure"})


if __name__ == '__main__':
    fire.Fire(updateService)
