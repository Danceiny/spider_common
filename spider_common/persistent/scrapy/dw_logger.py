# -*- coding: utf-8 -*-
import json
import requests
from six.moves.urllib.parse import (urlencode, urljoin)

from parser_engine.patch import get_redis
from parser_engine.singleton import Singleton
from parser_engine.utils import load_scrapy_settings
import logging

logger = logging.getLogger("dw_logger")


def log_to_dw(eventlog_base_url, action, **data):
    for k, v in data.items():
        if v is None:
            data[k] = ''
    url = eventlog_base_url + action + '?' + urlencode(data)
    retry_times = 2
    while retry_times > 0:
        try:
            resp = requests.get(url)
            if resp.status_code == requests.codes.ok:
                return True
            else:
                logger.warning("【%s】 log_to_dw failed, response status: %s", action, resp.status_code)
        except Exception as e:
            logger.error("【%s】 log_to_dw %s request exception: %s", action, str(e))
        retry_times -= 1


@Singleton
class DwLogger:
    def __init__(self, settings=None):
        settings = settings if settings else load_scrapy_settings()
        self.r = get_redis(**settings.get('REDIS_PARAMS', {"url": "redis://127.0.0.1:6379"}))
        self.ENV = settings.get('ENV')
        self.actions = settings.get('DW_ITEMS_CONFIG', {}).keys()
        self.active_fp = {}
        if self.ENV == 'local':
            for action in self.actions:
                self.active_fp[action] = open('dw_local_' + action + '.json', 'a+')

        conf = settings.get('DW_EVENTLOG_CONFIG', {}).copy()
        url = conf.pop('url')
        self.eventlog_common_data = conf
        self.eventlog_base_url = url if url.endswith('/') else url + '/'

    def __del__(self):
        for action, fp in self.active_fp.items():
            fp.close()

    def log_to_dw(self, action, **data):
        # dev环境才打数据到dw, local环境直接写文件
        if self.ENV == 'local':
            if action in self.active_fp:
                self.active_fp[action].write(json.dumps(data) + '\n')
            return
        data.update(self.eventlog_common_data)

        if log_to_dw(self.eventlog_base_url, action, **data):
            logger.info("%s success" % action)
        else:
            # 错误暂时记在redis中
            self.r.lpush('faillog:dw:' + action, json.dumps(data))
