# -*- coding: utf-8 -*-
import scrapy


class BetCoUkSpider(scrapy.Spider):
    name = 'bet_co_uk'
    allowed_domains = ['www.21bet.co.uk']
    start_urls = ['https://www.21bet.co.uk/sportsbook/SOCCER/EU_CL/']

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        json_data = {}

        for data in response.css('div.app--market__entry'):
            print("data>>>>>", data.extract())
            json_data[data.css('span.app--market__entry__name::text').extract().strip()
            ] = data.css('span.app--market__entry__value::text').extract().strip()

        with open("{}.json".format(self.name), 'w') as fj:
            import json
            fj.write(json.dumps(json_data))
        self.log('Saved file %s' % "{}.json".format(self.name))
