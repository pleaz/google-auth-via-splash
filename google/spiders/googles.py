# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest


class GooglesSpider(scrapy.Spider):
    name = 'googles'
    allowed_domains = ['google.com']
    start_urls = ['http://google.com/']
    req = 10
    series = {}

    def start_requests(self):
        script = """
        function main(splash)
            local url = splash.args.url
            assert(splash:go(url))
            assert(splash:wait(10))
    
            splash:set_viewport_full()
    
            local search_input = splash:select('input[name=identifier]')   
            search_input:send_text("mail@gmail.com")
            assert(splash:wait(5))
            local submit_button = splash:select('div[id=identifierNext]')
            submit_button:click()
            
            assert(splash:wait(10))
            
            local search_input_t = splash:select('input[name=password]')   
            search_input_t:send_text("")
            assert(splash:wait(5))
            local submit_button = splash:select('div[id=passwordNext]')
            submit_button:click()
    
            assert(splash:wait(10))
    
            return {
                html = splash:html(),
                png = splash:png(),
            }
          end
        """
        yield SplashRequest(
            'https://accounts.google.com/signin/v2/identifier?hl=en&passive=true&flowName=GlifWebSignIn&flowEntry=ServiceLogin',
            #callback = self.after_login,      ###inserting callabck
            endpoint='execute',
            args={
                'lua_source': script,
                'ua': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36"
            }
        )

    def parse(self, response):
        script = response.body