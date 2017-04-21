# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item

# export item by json
class JsonExpoterPipline(object):
    def __init__(self):
        self.file = open("article_items.json","wb")
        self.export = JsonItemExporter(self.file,encoding="utf-8",ensure_ascii=False)
        self.export.start_exporting()

    def close_spider(self):
        self.export.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.export.export_item(item)
        return item

# get images local path
class ArticleImagesPipline(ImagesPipeline):
    def item_completed(self, results, item, info):
        for ok,v in results:
            item['cover_local_path'] = v['path']
        return item
