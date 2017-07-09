# -*- coding: utf-8 -*-
import os
import scrapy
from scrapy.spider import Spider
from score_crawl.spiders import ROOT_DIR


class BetCoUkSpider(Spider):
    name = 'bet_co_uk'
    allowed_domains = ['www.21bet.co.uk']
    start_urls = ['https://www.21bet.co.uk/sportsbook/SOCCER/EU_CL/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = {}
        for data in response.css('li'):
            print("%%%%%%%%%%%%%%%%%", data.extract())
        for data in response.css('div.app--market__entry'):
            print("___________>>>>>>_________", data)
            json_data[data.css('span.app--market__entry__name::text').extract().strip()
            ] = data.css('span.app--market__entry__value::text').extract(

            ).strip()

        p = os.path.join(ROOT_DIR, "json_data/{}.json".format(self.name))

        with open(p, 'w+') as fj:
            import json
            fj.write(json.dumps(json_data))
        self.log('Saved file %s' % "{}.json".format(self.name))
