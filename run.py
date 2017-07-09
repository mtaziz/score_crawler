import json
import os
import schedule
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from twisted.internet import defer

from score_crawl.spiders import ROOT_DIR
from score_crawl.spiders.paddypower_com import PaddypowerComSpider
from score_crawl.spiders.sports_williamhill_com import SportsWilliamhillComSpider
from score_crawl.spiders.sportsbet_com_au import SportsBetComAuSpider


spider_list = [PaddypowerComSpider, SportsBetComAuSpider, SportsWilliamhillComSpider]


def print_matrix():
    matrix = {}
    for spider in spider_list:
        spider_data = json.loads(
            open(os.path.join(ROOT_DIR, "json_data/{}.json".format(spider.name)), "r").read()
        )
        for k, v in spider_data.items():
            if matrix.get(k):
                matrix[str(k).lower()].append((spider.name, v))
            else:
                matrix[str(k).lower()] = [(spider.name, v)]

    spider_map = {spider.name: index for index, spider in enumerate(spider_list)}

    header = "Sites:" + " " * 8
    for site in spider_map.keys():
        header += site + " " * 8

    print(header)
    for k, v in matrix.items():
        for site, value in v:
            print("Team: " + k + " " * 8 * spider_map[site] + " " * 8 + value)


def run_spiders():
    configure_logging()
    runner = CrawlerRunner()

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(PaddypowerComSpider)
        yield runner.crawl(SportsWilliamhillComSpider)
        yield runner.crawl(SportsBetComAuSpider)

    crawl()
    print_matrix()


schedule.every(5).seconds.do(run_spiders)

while True:
    schedule.run_pending()
