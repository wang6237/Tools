# -*- coding: utf8 -*-
import requests, json
import urllib.parse
from elasticsearch import Elasticsearch
import time
import datetime



def send_es(data):
    timestamp = datetime.date.today().strftime("%Y-%m-%d")
    index = "colorv-video-" + timestamp
    es = Elasticsearch(
        [
            {'host': '172.21.80.11', 'port': 9200}
        ]
        # ,
        # http_auth=('elastic', 'Ops@colorv.com!')
    )

    if not es.indices.exists(index):
        mapping = {
            "mappings": {
                "properties": {
                    "geoip": {
                        "properties": {
                            "location": {
                                "type": "geo_point"
                            }
                        }
                    }
                }
            }
        }
        

        es.indices.create(index, ignore=400, body=mapping)
    res = es.index(index=index, body=data, op_type='create', pipeline='geoip')
    return True


def main_handler(event, context):

    stime = time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(event['Records'][0]['event']['eventTime']))
    deleted = False
    deletedTime = None
    if 'cos:ObjectRemove:Delete' == event['Records'][0]['event']['eventName']:
        deleted = True
        deletedTime = stime
    dest = {
        'appid': event['Records'][0]['cos']['cosBucket']['appid'],
        'region': event['Records'][0]['cos']['cosBucket']['cosRegion'],
        'bucket': event['Records'][0]['cos']['cosBucket']['name'],
        'key': ('/').join(event['Records'][0]['cos']['cosObject']['key'].split('/')[3:]),
        'firstDir': event['Records'][0]['cos']['cosObject']['key'].split('/')[3],
        'size': event['Records'][0]['cos']['cosObject']['size'],
        'eventName': event['Records'][0]['event']['eventName'],
        'eventTime': stime,
        '@timestamp': stime,
        'isDeleted': deleted,
        'deleteTime': deletedTime,
        'requestSourceIP': event['Records'][0]['event']['requestParameters']['requestSourceIP'],
        'requestHeaders': event['Records'][0]['event']['requestParameters']['requestHeaders'],
        'url': event['Records'][0]['cos']['cosObject']['url']
    }
    send_es(dest)

    return "Hello World"

