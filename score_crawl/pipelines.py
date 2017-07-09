# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ScoreCrawlPipeline(object):
    def process_item(self, item, spider):
        print('GGGGGGGGG>>>>>>>>>', spider)
        return spider

    def close_spider(self, spider):
        print('GGGGGGGGG>>>>>>>>>', spider)
