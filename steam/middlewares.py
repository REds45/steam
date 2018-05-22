# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import  requests

class SteamSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SteamDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



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
        if request.meta.get('retry_times'):
            proxy=self.get_proxy()
            if proxy:
                uri='https://{}'.format(proxy)
                print('正在使用代理'+proxy)
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


    def process_response(self, request, response, spider):

        return response

    def process_exception(self, request, exception, spider):

        pass
    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)