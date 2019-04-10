from scrapy.downloadermiddlewares.retry import RetryMiddleware
from ..api import ClueApi


class ClueRetryMiddleware(RetryMiddleware):
    @classmethod
    def from_crawler(cls, crawler):
        cls.api = ClueApi()

    def _retry(self, request, reason, spider):
        ret = super()._retry(request, reason, spider)
        if ret:
            return ret
        # failed clue
        clue_id = request.meta.get('clue_id')
        if clue_id:
            clue = self.api.get_by_id(clue_id)
            if clue['status'] == 200:
                spider.debug("!!!retry a successful clue!!!")
            else:
                clue.fail()
                self.api.update(clue)
