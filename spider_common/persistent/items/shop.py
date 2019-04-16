from scrapy.item import Field
from .base import BaseItem


class ShopItem(BaseItem):
    city = Field()
    address = Field()
    cellphone = Field()
    telephone = Field()


