# -*- coding: utf-8 -*-
import scrapy
from score_crawl.spiders import ROOT_DIR
import os


class SportsWilliamhillComSpider(scrapy.Spider):
    name = 'sports_williamhill_com'
    allowed_domains = ['sports.williamhill.com']
    start_urls = ['http://sports.williamhill.com/bet/en-gb/betting/g/9067/Outright.html']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = {}

        for data in response.css('tr.rowOdd'):
            names = []
            for name in data.css('td.leftPad > div::text').extract():
                names.append(name.strip())
            prices = []
            for price in data.css('div.eventprice::text').extract():
                prices.append(price.strip())
            for index in range(len(names) - 1):
                json_data[names[index]] = prices[index]
        p = os.path.join(ROOT_DIR, "json_data/{}.json".format(self.name))

        with open(p, 'w+') as fj:
            import json
            fj.write(json.dumps(json_data))
        self.log('Saved file %s' % "{}.json".format(self.name))
