from .dw_logger import DwLogger
from parser_engine.itemclassloader import ItemClassLoader
from parser_engine.utils import load_scrapy_settings


class DwPipeline(object):

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        obj = cls(settings=crawler.settings)
        return obj

    def __init__(self, action=None, item_cls=None, settings=None):
        self.item_loader = None
        self.logger = None
        self.item_configs = None

        self.setup_from_settings(settings=settings if settings else load_scrapy_settings())
        if action and item_cls:
            self.item_configs.update({
                action: self.item_loader.get(item_cls),
            })

    def setup_from_settings(self, settings):
        self.item_loader = ItemClassLoader(settings=settings)
        self.logger = DwLogger(settings=settings)
        conf = settings.get('DW_ITEMS_CONFIG')
        if conf:
            item_configs = {}
            for action, item_cls in conf.items():
                item_configs[action] = self.item_loader.get(item_cls)
            self.item_configs = item_configs

    def process_item(self, item, spider):
        if self.item_configs:
            for action, item_cls in self.item_configs.items():
                if isinstance(item, item_cls):
                    self.logger.log_to_dw(action, **item)
        return item
