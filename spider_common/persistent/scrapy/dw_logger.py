# -*- coding: utf-8 -*-
import json
import requests
from six.moves.urllib.parse import (urlencode)

from parser_engine.patch import get_redis
from parser_engine.singleton import Singleton
from parser_engine.utils import load_scrapy_settings


@Singleton
class DwLogger:
    def __init__(self, settings=None, write_filename='dw_local.txt'):
        settings = settings if settings else load_scrapy_settings()
        self.r = get_redis(**settings.get('REDIS_PARAMS', {"url": "redis://127.0.0.1:6379"}))
        self.ENV = settings.get('ENV')
        if write_filename:
            self.f = open(write_filename, 'a+')
        else:
            self.f = None

    def __del__(self):
        if getattr(self, 'f', None):
            self.f.close()

    def log_to_dw(self, action, **data):
        if self.ENV == 'local':
            if self.f:
                self.f.write(json.dumps(data) + '\n')
            return

        # dev环境才打数据到dw
        data['event_type'] = 'bxmainsite_aux'
        data['site_id'] = 'bx_crawler'
        data['tracktype'] = 'event'
        data['__debug'] = 1
        url = 'https://www.baixing.com/c/aux/' + action + '?' + urlencode(data)

        resp = requests.get(url)
        retry_times = 2
        while retry_times > 0 and resp.status_code != requests.codes.ok:
            resp = requests.get(url)
            retry_times -= 1

        if resp.status_code != requests.codes.ok:
            # 错误暂时记在redis中
            self.r.set('faillog:dw:' + action, json.dumps(data))
