# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import  requests


class SteamProxyMiddleware(object):

    @classmethod
    def from_crawler(cls, crawler):
        settings= crawler.settings
        return cls(
            proxy_url=settings.get('PROXY_URL')
        )
    def __init__(self,proxy_url):
        self.proxy_url=proxy_url

    def get_proxy(self):
        try:
            response=requests.get(self.proxy_url)
            if(response.status_code==200):
                proxy=response.text
                return proxy
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        if request.meta.get('retry_times')or request.meta.get('proxy'):
            proxy=self.get_proxy()
            if proxy:
                uri='https://{}'.format(proxy)
                print('正在使用代理'+proxy)
                with open('error.txt', 'a+') as file:
                    file.write('使用代理'+proxy)
                request.meta['proxy']=uri



    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):

        pass
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SteamCookieMiddleware(object):


    def process_request(self, request, spider):
        cookie={
            'mature_content':'1',
            'steamCountry' :'CN|9a84f1db057c0a8283337854148dbc88',
            'birthtime':'631123201',
            'lastagecheckage': '1-January-1990'
        }
        request.cookies=cookie
        request.headers['Accept-Language']='zh-CN,zh;q=0.9'


    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):

        pass
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)






