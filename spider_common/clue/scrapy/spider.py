from parser_engine.spider import PESpider
from ..api import ClueApi, ApiCallException


class ClueSpider(PESpider):
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = super(ClueSpider, cls).from_crawler(crawler, *args, **kwargs)
        cls.api = ClueApi()
        return obj

    def finish_clue(self, response, dw_count=0):
        """

        :param response:
        :param dw_count:
        """
        meta = response.meta
        clue_id = meta.get('clue_id')
        self.log("after yield, update clue_id: %s" % clue_id)
        if clue_id:
            try:
                clue = self.api.get_by_id(clue_id)
            except ApiCallException as e:
                self.error("clue_id: {clue_id} not found, exception: {e}".format(clue_id=clue_id, e=str(e)))
                return
            clue.success()
            clue.dw_count = dw_count
            if not self.api.update(clue):
                raise Exception("update clue %d failed" % clue.id)
