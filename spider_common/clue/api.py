from parser_engine.singleton import Singleton
import requests
from .models import Clue
from ..common_utils import ApiCallException, InitArgsException


@Singleton
class ClueApi:
    def __init__(self, **kwargs):
        self.api = kwargs.pop('api')
        if not self.api:
            raise InitArgsException("ClueApi no api config")

    def _switch(self, api):
        self.api = api

    def get_by_id(self, clue_id):
        resp = requests.get(self.api + '/' + str(clue_id))
        if resp.status_code == 200 and resp.json()['code'] == 0:
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

    def create(self, data, project=None, spider=None, from_clue_id=0):
        """

        :param data:
        :param project:
        :param spider:
        :param from_clue_id:
        :return: [{clue}]
        """
        if isinstance(data, list) and project is not None and spider is not None:
            resp = requests.post(url=self.api + '/',
                                 json={'project': project, 'spider': spider, 'from_clue_id': from_clue_id,
                                       'clues': data})
        else:
            resp = requests.post(url=self.api + '/',
                                 json={'project': data.pop('project', data.pop('channel')),
                                       'spider': data.pop('spider', data.pop('name')),
                                       'from_clue_id': data.pop('from_clue_id', 0),
                                       'clues': [data]})
        if resp.status_code == 200 and resp.json()['code'] == 0:
            return [Clue(item) for item in resp.json()['data']]
        else:
            raise ApiCallException('create clue failed', resp.status_code)
