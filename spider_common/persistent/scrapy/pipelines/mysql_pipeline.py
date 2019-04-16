from peewee import Model, PrimaryKeyField, IntegerField, CharField, ProgrammingError
from parser_engine.config import mysqldb
from ...items.shop import ShopItem
from playhouse.shortcuts import dict_to_model, model_to_dict


class ShopTable(Model):
    id = PrimaryKeyField()
    crawled_time = IntegerField(verbose_name="抓取时间", default=0)
    src = CharField(verbose_name="来源渠道", max_length=32, default='')  # 约定的统一名称
    src_id = CharField(verbose_name="来源渠道的原始id", max_length=64, default='')
    name = CharField(verbose_name="店铺名称", max_length=64, default='')
    cellphone = CharField(verbose_name="手机", max_length=64, default=0)
    city = CharField(verbose_name="状态", max_length=32, default=0)
    address = CharField(verbose_name="创建时间", max_length=255, default=0)
    telephone = CharField(verbose_name="固定电话", max_length=64, default=0)
    channel = CharField(verbose_name="业务渠道", max_length=32, default='')

    class Meta:
        table_name = 'shop'
        database = mysqldb


class ShopMySQLPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, ShopItem):
            try:
                model = ShopTable.get_or_none(src_id=item.get('src_id'), src=item.get('src'))
                if model:
                    # 将 item 没有的属性从 model 中补全
                    for k, v in model_to_dict(model).items():
                        value = item.get(k)
                        if not value:
                            item[k] = v
                    ShopTable.update(**item).where(ShopTable.id == model.id).execute()
                else:
                    model = dict_to_model(ShopTable, item, True)
                    model.save()
            except Exception as e:
                if isinstance(e, ProgrammingError) and not ShopTable.table_exists():
                    ShopTable.create_table()
                spider.error("Shop MySQL pipeline failed, exception: %s" % str(e))
                print(item)
        return item
