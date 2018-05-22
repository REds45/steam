# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from steam.items import ListItem,DetailItem

class SteamPipeline(object):
    def __init__(self,host,dbname):
        self.host=host
        self.dbname=dbname
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.host)
        self.db = self.client[self.dbname]
        self.db[DetailItem.collection].create_index([('game_id',pymongo.ASCENDING)])

    def process_item(self, item, spider):
        if isinstance(item,ListItem):
            self.db[item.collection].insert(dict(item))
        if isinstance(item,DetailItem):
            self.db[item.collection].update({'game_id':item.get('game_id')},{'$set':dict(item)},True)
    def close_spider(self, spider):
        self.client.close()

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            host=crawler.settings.get('MONGO_HOST'),
            dbname=crawler.settings.get('MONGO_DB'),
        )
