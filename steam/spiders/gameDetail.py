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
        if( '/sub'in response.url or '/bundle'in response.url) :
            return
        try:
            item = DetailItem()
            item['name'] = response.xpath('//div[@class="apphub_AppName"]/text()').extract()[0]
            if (response.xpath(
                    '//*[@id="game_area_purchase"]//div[contains(@class,"final_price")]/text()').extract() != []):
                item['price'] = \
                    response.xpath(
                        '//*[@id="game_area_purchase"]//div[contains(@class,"final_price")]/text()').extract()[
                        0].strip().strip("¥ ")
            else:
                item['price'] = \
                    response.xpath('//*[@id="game_area_purchase"]//div[contains(@class,"price")]/text()').extract()[
                        0].strip().strip("¥ ")

            item['description'] = response.xpath('//*[@id="game_area_description"]').xpath('string(.)').extract()[0] \
                .replace("\t", "").replace("\r\n", "")
            if (response.xpath(
                    '//*[@id="game_highlights"]//span[contains(@class,"nonresponsive_hidden")]').extract() == []):
                item['review'] = '无用户评测'
            else:
                item['review'] = \
                    response.xpath(
                        '//*[@id="game_highlights"]//span[contains(@class,"nonresponsive_hidden")]').extract()[0] \
                        .replace("\t", "").replace("\r\n", "")
            item['game_id'] = response.url.split("/")[-3]
        except:

            return Request(response.url,meta={'retry_times':1},callback=self.parse_detail())

        yield item










