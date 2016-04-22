#!/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'wangyk'

import commands,time
import threading
from multiprocessing import Process
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

# 可以屏蔽一些已关闭的工程
bad_list = []

class conn_ice_grid(object):
    def __init__(self,ice_grid_server,ice_grid_port,default_Locator_name):
        self.user = 'admin'
        self.password = 'xxxx'  #密码
        self.grid_server = ice_grid_server
        self.grid_port = ice_grid_port
        self.default_Locator = default_Locator_name
        self.run()

    def get_server_list(self):
        # 获取在线server的列表
        print "start get server list"
        server_list_cmd = "icegridadmin --Ice.Default.EncodingVersion=1.0 --Ice.Default.Locator='%sIceGrid/Locator:tcp -h %s -p %s' -u %s -p '%s' -e 'server  list'" % (self.default_Locator,self.grid_server,self.grid_port,self.user,self.password)
        server_list = commands.getstatusoutput(server_list_cmd)[1].split('\n')
        if len(server_list) == 0 :
            self.sendmail("获取ICE Server 失败！！，请见检查服务器")
        self.s_list = []
        for k in server_list:
            if "icegridadmin" in k:
                pass
            else:
                # 判断是否在bad_list中
                if k in bad_list:
                    pass
                else:
                    self.s_list.append(k)
    def monitor(self):
        print "check server"
 #       print self.s_list

        for service_name in self.s_list:
            server_state_cmd = "icegridadmin --Ice.Default.EncodingVersion=1.0 --Ice.Default.Locator='%sIceGrid/Locator:tcp -h %s -p %s'  -u %s -p '%s' -e 'server  state %s'" % (self.default_Locator,self.grid_server,self.grid_port,self.user,self.password,service_name)
            for k1 in commands.getstatusoutput(server_state_cmd)[1].split('\n'):
                if  k1.startswith("error:"):
                    #print service_name
                    msg = "%s %s is Warning on %s %s"  % (service_name,k1,self.grid_server,self.default_Locator)

                    if service_name in bad_list:
                        print "\033[41;1m %s\033[0m" % msg
                    else:
                        print "start mail...."
                        self.sendmail(msg)

                elif  k1.startswith("active") and "enabled" in k1:
                    print "%s: \033[32;1m %s %s  is OK\033[0m" % (time.ctime(),service_name,k1)
                else:
                    pass

    def sendmail(self,*args):  #邮箱需要重新定义
        msg = MIMEText(args[0], 'plain', 'utf-8')
        msg['From'] = formataddr(["ICE 监控告警",'alarm1@test.com'])
        msg['To'] = formataddr(["用户","运维监控中心"])
        msg['Subject'] = "ICE 监控告警"

        server = smtplib.SMTP("smtp.sina.com", 25)
        server.login("alarm1@sina.com", "usr/index_usr.jsp")
        server.sendmail('alarm1@sina.com', ['yunwei@sina.com',], msg.as_string())
        server.quit()

    def run(self):
        print "Start...."
  #      print self.grid_server,self.grid_port,self.default_Locator
        while True:
            self.get_server_list()
            self.monitor()
            print "waiting"
            time.sleep(60)



if __name__ == "__main__":

    #使用线程
    t1 = threading.Thread(target=conn_ice_grid,args=("172.16.30.x","4061","Account"))
    t1.start()

    t3 = threading.Thread(target=conn_ice_grid,args=("172.16.30.x","4061","Business"))
    t3.start()



