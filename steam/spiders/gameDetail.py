# -*- coding: utf-8 -*-
from steam.items import ListItem , DetailItem
from scrapy import  Spider,Request
from bs4 import BeautifulSoup
import requests
class GamedetailSpider(Spider):
    name = 'gameDetail'

    def start_requests(self):
        url = 'https://store.steampowered.com/search/?os=win&filter=globaltopsellers&page={}'
        for i in range(1,self.settings.get('PAGE')+1):
            yield Request(url.format(i),callback=self.parse_list)

    def parse_list(self, response):
        item=ListItem()
        soup=BeautifulSoup(response.text,'lxml')
        nameList=soup.select('div.col.search_name.ellipsis > span')
        urlList=soup.select('#search_result_container a[class^="search"]')
        for game,url in zip(nameList,urlList):
            item['game_name']=game.get_text()
            item['url']=url.get('href')
            yield item
            yield Request(item['url'],callback=self.parse_detail)


    def parse_detail(self, response):
        if('站点错误' in response.text):
            with open('error.txt', 'a+') as file:
                file.write(response.url+"您所在的地区目前不提供此物品，使用代理访问")
            return Request(response.url,meta={'proxy':1},callback=self.parse_detail)
        if ('/sub' in response.url or '/bundle' in response.url):
            return
        try:
            item = DetailItem()
            item['name'] = response.css('div.apphub_AppName ::text').extract()[0]
            if (response.css('div.game_purchase_price.price')):
                price = response.css('div.game_purchase_price.price ::text')
            else:
                price = response.css('#game_area_purchase div.discount_original_price ::text')
            item['price'] = int(price.extract()[0].strip().strip('¥ '))
            if (response.css('span.nonresponsive_hidden.responsive_reviewdesc')):
                item['review'] = response.css('span.nonresponsive_hidden.responsive_reviewdesc ::text').extract()[
                    0].strip()
            else:
                item['review'] = '无用户评测'
            item['description'] = response.css('#game_area_description').xpath('string(.)').extract()[0].replace("\r",
                                                                                                                 " ").replace(
                "\n", " ").replace("\t", " ")
            item['game_id'] = response.url.split('/')[-3]
            yield item
        except Exception as e:
            with open ('error.txt','a+') as file:
                file.write(response.url+'\n   error Info:'+repr(e)+'\n')












