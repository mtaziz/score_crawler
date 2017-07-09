# -*- coding: utf-8 -*-
import os
import scrapy
from score_crawl.spiders import ROOT_DIR


class PaddypowerComSpider(scrapy.Spider):
    name = 'paddypower_com'
    allowed_domains = ['www.paddypower.com']
    start_urls = ['http://www.paddypower.com/football/euro-football/champions-league']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = {}

        rdata = response.css('div.fb-sub-content')
        for data in rdata:
            for item in data.css('div.fb-odds-group.item > span.odd'):
                json_data[item.css('span.odds-label::text').extract()[0].strip()
                ] = item.css('span.odds-value::text').extract()[0].strip()

        p = os.path.join(ROOT_DIR, "json_data/{}.json".format(self.name))

        with open(p, 'w+') as fj:
            import json
            fj.write(json.dumps(json_data))
        self.log('Saved file %s' % "{}.json".format(self.name))
