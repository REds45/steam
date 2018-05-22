# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import  Item,Field


class ListItem(Item):
    collection='gameList'
    game_name=Field()
    url=Field()
class DetailItem(Item):
    collection='gameDetail'
    name=Field()
    price=Field()
    description=Field()
    review=Field()
    game_id=Field()

