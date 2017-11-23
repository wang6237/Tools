#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests
import sys, json

# 钉钉机器人的token url
DD_URL='https://oapi.dingtalk.com/robot/send?access_token=xxxxxxx'
# message模板，主要是替换content的内容
#msg_template={"msgtype": "text", "text": {"content": "大家好！看我头像就知道我是谁了吧"}, "at": {"atMobiles": ["186xxxxx87"],"isAtAll": False}}
msg_template={"msgtype": "text", "text": {"content": "大家好！看我头像就知道我是谁了吧"}}
# 设置header 
headers={'Content-Type': 'application/json'}

def send_dd():
	if len(sys.argv)>1:
		msg=sys.argv[1]
		msg_template['text']['content']=msg
		r = requests.post(DD_URL,json.dumps(msg_template),headers=headers)
		#print r.text
	else:
		exit()


if __name__ == "__main__":
	send_dd()

#[root@nagios ~]# /usr/bin/send_dd.py "为人民服务！"
#{"errcode":0,"errmsg":"ok"}
