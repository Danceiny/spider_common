from .items import ClueItem
from ..api import ClueApi
from ..models import Clue


# persistent Clue
class CluePersistentPipeline(object):
    def __init__(self):
        self.api = ClueApi()

    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            clue = self.api.create(Clue.from_item(item))[0]
            item['req'].meta['clue_id'] = clue.id
            spider.info('CluePersistentPipeline save clue {clue_id} to database'
                        .format(clue_id=item['req'].meta.get('clue_id')))
        return item


# route clue to queue
class CluePipeline(object):

    def process_item(self, item, spider):
        if isinstance(item, ClueItem):
            clue_id = item['req'].meta.get('clue_id')
            spider.info('CluePipeline route clue {clue_id} to queue'.format(clue_id=clue_id))
            spider.route('%s:%s:start_urls' % (item['project'], item['spider']), item['req'])
        return item
