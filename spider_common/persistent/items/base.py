from scrapy.item import Item, Field


class BaseItem(Item):
    name = Field()
    channel = Field()  # 英文 线索渠道的业务名称
    crawled_time = Field()
    src_id = Field()  # 来源渠道中的唯一id
    src = Field()  # 来源渠道
