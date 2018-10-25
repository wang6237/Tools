#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import time
import fire
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

rancher_server_url = 'http://xx.xxx.xxx.xxx:9000/v2-beta/projects'
access_key = 'xxxxxxxxxxxxxxx'
secret_key = 'yyyyyyyyyyyyyyyyyyysfaf'

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
        # print(r.text)
        return r.json()

class updateService(object):
    def __init__(self):
        pass

    def _send_mail(self, msgs, email='xxxx@cccc.com'):
        # smtp服务器
        host_server = 'mail.qq.com'
        # sender_qq为发件人的qq号码
        sender_qq = 'mailer@qq.com.cn'
        # pwd为邮箱的授权码
        pwd = 'mail@xxxxx.com'  ##
        # 发件人的邮箱
        sender_qq_mail = 'mailer@qq.com.cn'
        # 收件人邮箱
        receiver = email

        # 邮件的正文内容
        mail_content = msgs
        # 邮件标题
        mail_title = msgs

        # 邮件正文内容
        msg = MIMEMultipart()
        # msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = 'NagiosServer'
        msg["To"] = Header('管理员', 'utf-8')  ## 接收者的别名

        # 邮件正文内容
        msg.attach(MIMEText(mail_content, 'html', 'utf-8'))

        # ssl登录
        # smtp = smtplib.SMTP_SSL(host_server)
        smtp = smtplib.SMTP(host_server, 587)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(0)
        smtp.starttls()
        smtp.login(user='mailer@xxx.com', password='mail@xxxxxm')
        

        smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
        smtp.quit()

    def update(self,imageUuid, project_id, service_id):
        """接收，service upgraded的url、imageUuid、environment、service state，
        根据url获取到，service的url，=> service state =>
        """
        action_url = rancher_server_url + '/' +project_id + '/services/' + service_id + '/?action'
        upgrade_strategy = json.loads(
            '{"inServiceStrategy": {"batchSize": 1,"intervalMillis": 10000,"StartFirst": true,"launchConfig": {},"secondaryLaunchConfigs": []}}')

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
            msg = "%s Update Service Succeed" % service_info['name']
            # self._send_mail(msg)
            return json.dumps({'msg': msg})
        else:
            msg = "%s Update Service Succeed" % service_info['name']
            self._send_mail(msg)
            return json.dumps({'msg': "Update Service Failure"})


if __name__ == '__main__':
    fire.Fire(updateService)
