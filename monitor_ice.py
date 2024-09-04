#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangyk'

import subprocess
import time
import threading
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import configparser

# 可以屏蔽一些已关闭的工程
bad_list = []

class ConnIceGrid(object):
    def __init__(self, ice_grid_server, ice_grid_port, default_locator_name):
        self.user = 'admin'
        self.password = 'xxxx'  # 密码
        self.grid_server = ice_grid_server
        self.grid_port = ice_grid_port
        self.default_locator = default_locator_name
        self.run()

    def get_server_list(self):
        # 获取在线server的列表
        print("start get server list")
        server_list_cmd = f"icegridadmin --Ice.Default.EncodingVersion=1.0 --Ice.Default.Locator='{self.default_locator}IceGrid/Locator:tcp -h {self.grid_server} -p {self.grid_port}' -u {self.user} -p '{self.password}' -e 'server list'"
        server_list = subprocess.getoutput(server_list_cmd).split('\n')
        if not server_list:
            self.sendmail("获取ICE Server 失败！！，请检查服务器")
        self.s_list = [k for k in server_list if "icegridadmin" not in k and k not in bad_list]

    def monitor(self):
        print("check server")
        for service_name in self.s_list:
            server_state_cmd = f"icegridadmin --Ice.Default.EncodingVersion=1.0 --Ice.Default.Locator='{self.default_locator}IceGrid/Locator:tcp -h {self.grid_server} -p {self.grid_port}' -u {self.user} -p '{self.password}' -e 'server state {service_name}'"
            state_output = subprocess.getoutput(server_state_cmd).split('\n')
            for k1 in state_output:
                if k1.startswith("error:"):
                    msg = f"{service_name} {k1} is Warning on {self.grid_server} {self.default_locator}"
                    if service_name not in bad_list:
                        print(f"\033[41;1m {msg}\033[0m")
                        self.sendmail(msg)
                elif k1.startswith("active") and "enabled" in k1:
                    print(f"{time.ctime()}: \033[32;1m {service_name} {k1} is OK\033[0m")

    def sendmail(self, message):
        msg = MIMEText(message, 'plain', 'utf-8')
        msg['From'] = formataddr(["ICE 监控告警", 'alarm1@test.com'])
        msg['To'] = formataddr(["用户", "运维监控中心"])
        msg['Subject'] = "ICE 监控告警"

        server = smtplib.SMTP("smtp.sina.com", 25)
        server.login("alarm1@sina.com", "usr/index_usr.jsp")
        server.sendmail('alarm1@sina.com', ['yunwei@sina.com'], msg.as_string())
        server.quit()

    def run(self):
        print("Start....")
        while True:
            self.get_server_list()
            self.monitor()
            print("waiting")
            time.sleep(60)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config.ini')

    t1 = threading.Thread(target=ConnIceGrid, args=(config['IceGrid']['Server1'], config['IceGrid']['Port1'], config['IceGrid']['Locator1']))
    t1.start()

    t3 = threading.Thread(target=ConnIceGrid, args=(config['IceGrid']['Server2'], config['IceGrid']['Port2'], config['IceGrid']['Locator2']))
    t3.start()
