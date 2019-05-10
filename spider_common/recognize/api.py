# -*- coding: utf-8 -*-

import json
import hashlib
import urllib
import urllib.request
import urllib.error
from .validator import params_type_check
from parser_engine.singleton import Singleton


@Singleton
class Api:
    @params_type_check
    def __init__(self, api_key: str, api_secret: str, biz_channel: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.biz_channel = biz_channel
        self.host = 'http://www.baixing.com'

    @params_type_check
    def _api(self, api_name: str, data: dict) -> dict:
        path = '/api/v2/' + api_name + '/'
        body = json.dumps(data)

        hash_code = hashlib.md5((path + body + self.api_secret).encode('utf-8')).hexdigest()

        headers = {
            'BAPI-APP-KEY': self.api_key,
            'BAPI-HASH': hash_code,
            'Content-Type': 'application/json'
        }

        url = self.host + path
        request = urllib.request.Request(url=url, headers=headers)

        try:
            res = urllib.request.urlopen(request, data=body.encode("utf-8"), timeout=10)
            return json.loads(res.read())['result']
        except urllib.error.HTTPError as e:
            if e.getcode() == 404:
                return json.loads(e.read())
            else:
                raise e

    @params_type_check
    def robot_recognize_content_v2(self, content: dict) -> dict:
        """
        通用打包内容识别机审v2接口，结果同步返回。
        支持文本，图片的审核和实体之间的任意组合识别

        :param content: 见文档详细字段解释
        :type content: dict
        :return: dict
        """
        data = {
            'bizChannel': self.biz_channel,
            'content': content
        }

        return self._api('Quality.robotRecognizeContentV2', data)

    @params_type_check
    def recognize_content_v2(self, content: dict) -> dict:
        """
        通用打包内容“机审+人审”识别接口，结果异步返回。
        支持文本，图片的审核和实体之间的任意组合识别

        :param content: 同Quality.robotRecognizeContentV2 接口
        :type content: dict
        :return: dict
        """
        data = {
            'bizChannel': self.biz_channel,
            'content': content
        }

        return self._api('Quality.recognizeContentV2', data)

    @params_type_check
    def recognize_contacts(self, values: dict) -> dict:
        """
        检测文本中是否含有QQ，微信，电话等联系方式，结果同步返回。

        :param values: 同Quality.robotRecognizeContentV2 接口
        :type values: dict
            {
                'index1': '卖一台二手笔记本，要的联系177-1754-0902，qq78087654',
                'index2':  '测试文本'
            }
        :return: dict
            {
                'recognizeId': 'chr:5cd52e4b33792f514c3b990a',
                'contentDecision': {
                    'label': '联系方式',
                    'probability': 1,
                    'content': [
                        {'entity': 'tanceiny', 'entityType': 'Weixin'}
                    ],
                    'status': 'accept',
                    'info': {'message': '内容涉及“联系方式”'}
                },
                'contentDecisionDetail': {
                    '1': {
                            'contact':
                                {
                                    'content': [
                                        {'entity': 'tanceiny', 'entityType': 'Weixin'}
                                    ],
                                    'label': '联系方式',
                                    'probability': 1,
                                    'status': 'accept',
                                    'info': {'message': '内容涉及“联系方式”'}
                                }
                         }
                }
            }

        """
        content = {}
        for index, text in values.items():
            content[index] = {
                'type': 'text',
                'value': text,
                'recognizeTypes': ['contact']
            }
        return self.robot_recognize_content_v2(content)

    @params_type_check
    def upload_customer_decision(self, recognize_id: str, status: str, label: str) -> bool:
        """
        回传业务侧最终操作结果，便于针对业务需求对模型进行调整和优化

        :param recognize_id: 详见Quality.robotRecognizeContent接口返回数据
        :type recognize_id: str
        :param status: accpet（通过）、refuse（拒绝）
        :type status: str
        :param label: 可协商约定
        :type label: str
        :return: False | True
        """
        data = {
            'bizChannel': self.biz_channel,
            'recognizeId': recognize_id,
            'status': status,
            'label': label,
        }

        return self._api('Quality.uploadCustomerDecision', data)

    @params_type_check
    def is_valid_callback(self, api_key: str, hash: str, dataStr: str) -> bool:
        """
        检查异步的审核结果确定是合法的回调

        :param api_key: headers 中的 BAPI-APP-KEY
        :type api_key: str
        :param hash: headers 中的 BAPI-HASH
        :type hash: str
        :param dataStr: post data str
        :type dataStr: str
        :return: False | True
        """
        if api_key != self.api_key:
            return False

        hash_code: str = hashlib.md5((dataStr + self.api_secret).encode('utf-8')).hexdigest()

        return hash_code == hash
