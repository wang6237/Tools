#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
-------------------------------------------------
   @File    : rabbitmqAdmin.py
   @Time    : 2020/09/22 10:15:01
   @Author  : wang6237
   @Contact : ykwang@vip.qq.com
   @Version : 0.1
   @Desc    : Rabbitmq Management UI API 
-------------------------------------------------
'''
__author__ = 'wang6237'

import requests


class rabbitmqManagement(object):
    '''
    Rabbitmq Management UI API
    '''
    def __init__(self, **kwargs):
        self.baseUrl = kwargs['baseUrl']
        self.auth = (kwargs['username'], kwargs['password'])

    def _get(self, url):
        try:
            response = requests.get(url, auth=self.auth)
            return response.json()
        except requests.exceptions.ConnectionError as e:
            return e

    def _put(self, url, data):
        headers = {
            'content-type': 'application/json',
        }
        try:
            response = requests.get(url,
                                    headers=headers,
                                    data=data,
                                    auth=self.auth)
            return response.json()
        except requests.exceptions.ConnectionError as e:
            return e

    def getOverview(self):
        '''
        Url: /api/overview
        Desc: Various random bits of information that describe the whole system.
        '''
        url = self.baseUrl + '/api/overview'
        return self._get(url)

    def getClusterName(self):
        '''
        Url: /api/cluster-name
        Desc: Name identifying this RabbitMQ cluster.
        '''
        url = self.baseUrl + '/api/cluster-name'
        return self._get(url)

    def getNodes(self):
        '''
        Url: /api/nodes	
        Desc: A list of nodes in the RabbitMQ cluster.
        '''
        url = self.baseUrl + '/api/nodes'
        return self._get(url)

    def getNode(self, name):
        '''
        Url: /api/nodes/name
        Desc: An individual node in the RabbitMQ cluster. Add "?memory=true" to get memory statistics, and "?binary=true" to get a breakdown of binary memory use (may be expensive if there are many small binaries in the system).
        '''
        url = self.baseUrl + '/api/nodes/name'
        return self._get(url)

    def getConnections(self):
        '''
        Url: /api/connections
        Desc: A list of all open connections.
        '''
        url = self.baseUrl + '/api/connections'
        return self._get(url)

    def getConnections_vhost(self, vhost):
        '''
        url: /api/vhosts/vhost/connections	
        Desc: A list of all open connections in a specific vhost.
        '''
        url = self.baseUrl + '/api/vhosts/' + vhost + '/connections'
        return self._get(url)

    def getChannels(self):
        '''
        url: /api/channels
        Desc: 	A list of all open channels.
        '''
        url = self.baseUrl + '/api/channels'
        return self._get(url)

    def getChannels_vhost(self, vhost):
        '''
        url: /api/vhosts/vhost/channels
        Desc: A list of all open channels in a specific vhost.
        返回一个列表
        '''
        url = self.baseUrl + '/api/vhosts/' + vhost + '/channels'
        return self._get(url)

    def getConsumers(self):
        '''
        url: /api/consumers
        Desc: A list of all consumers.
        '''
        url = self.baseUrl + '/api/consumers'
        return self._get(url)

    def getExchanges(self):
        '''
        url: /api/exchanges
        Desc: A list of all exchanges
        '''
        url = self.baseUrl + '/api/exchanges'
        return self._get(url)

    def getExchanges_vhost(self, vhost):
        '''
        url: /api/exchanges/vhost
        Desc: A list of all exchanges in a given virtual host.
        '''
        url = self.baseUrl + '/api/exchanges/' + vhost
        return self._get(url)

    def getExchanges_vhost_name(self, vhost, name):
        '''
        url: /api/exchanges/vhost/name
        Desc: An individual exchange. To PUT an exchange, you will need a body looking something like this:
                {"type":"direct","auto_delete":false,"durable":true,"internal":false,"arguments":{}}
                The type key is mandatory; other keys are optional.
                When DELETEing an exchange you can add the query string parameter if-unused=true. This prevents the delete from succeeding if the exchange is bound to a queue or as a source to another exchange.
        '''
        url = self.baseUrl + '/api/exchanges/' + vhost + '/' + name
        return self._get(url)

    def getVhost(self):
        '''
        url: /api/vhosts
        Desc: A list of all vhost
        '''
        url = self.baseUrl + '/api/vhosts'
        return self._get(url)

    def getVhost_name(self, name):
        '''
        url: /api/vhosts/name
        Desc: A vhost information
        '''
        url = self.baseUrl + '/api/vhosts/' + name
        return self._get(url)
