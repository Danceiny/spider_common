from parser_engine.singleton import Singleton
import requests
from .models import Clue
from ..common_utils import ApiCallException


@Singleton
class ClueApi:
    def __init__(self, **kwargs):
        self.api = kwargs.pop('api')

    def _switch(self, api):
        self.api = api

    def get_by_id(self, clue_id):
        resp = requests.get(self.api + '/' + str(clue_id))
        if resp.status_code == 200:
            return Clue(resp.json()['data'])
        elif resp.status_code == 404:
            raise ApiCallException(404)
        else:
            raise ApiCallException(resp.status_code)

    def partial_get_by_id(self, clue_id, keys):
        resp = requests.get(self.api + '/' + str(clue_id), {"keys": ','.join(keys)})
        if resp.status_code == 200 and resp.json()['code'] == 0:
            return resp.json()['data']
        elif resp.status_code == 404:
            raise ApiCallException(404)
        else:
            raise ApiCallException(resp.status_code)

    def update(self, data):
        clue_id = data.pop('id')
        resp = requests.put(self.api + '/' + str(clue_id), json=data)
        return resp.status_code == 200 and resp.json()['code'] == 0

    def create(self, data):
        resp = requests.post(self.api + '/', json=data)
        if resp.status_code == 200 and resp.json()['code'] == 0:
            return resp.json()['data']
        else:
            raise ApiCallException('create clue failed', resp.status_code)
