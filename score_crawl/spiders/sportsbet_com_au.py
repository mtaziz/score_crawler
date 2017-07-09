# -*- coding: utf-8 -*-
import os
import scrapy
from score_crawl.spiders import ROOT_DIR


class SportsBetComAuSpider(scrapy.Spider):
    name = 'sportsbet_com_au'
    allowed_domains = ['www.sportsbet.com.au']
    start_urls = [
        'http://www.sportsbet.com.au/betting/soccer/uefa-competitions/uefa-champions-league/Champions-League-Outright-2016-17-2710742.html'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = {}

        for data in response.css('div#accordion-body-327557'):
            json_data[data.css('div.market-buttons > div.price-link > a > '
                               'span.team-name.ib::text').extract()[0].strip()
            ] = data.css(
                'div.market-buttons > div.price-link > a > '
                'span.price-val_307224398.odd-val.ib.right::text'
            ).extract()[0].strip()

        p = os.path.join(ROOT_DIR, "json_data/{}.json".format(self.name))

        with open(p, 'w+') as fj:
            import json
            fj.write(json.dumps(json_data))
        self.log('Saved file %s' % "{}.json".format(self.name))
