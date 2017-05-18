# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi
import MySQLdb
import MySQLdb.cursors


class ArticlespiderPipeline(object):
    def process_item(self, item, spider):
        return item


# export item by json
class JsonExpoterPipline(object):
    def __init__(self):
        self.file = open("article_items.json", "wb")
        self.export = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
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
        if "cover_url" in item:
            for ok, v in results:
                item['cover_local_path'] = v['path']
        return item


# db pipline
class MysqlTwistedPipline(object):
    # init connect pool
    def __init__(self, connpool):
        self.connpool = connpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset="utf8",
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # connpool
        connpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        return cls(connpool)

    def process_item(self, item, spider):
        query = self.connpool.runInteraction(self.do_insert, item)
        # excepion handler
        query.addErrback(self.error_handler)

    def error_handler(self,failure):
        print(failure)

    def do_insert(self, cursor, item):
        # insert_sql = """
        #     insert into article (article_title,article_date,url_id,vote_num,cover_url,article_tags)
        #     values(%s,%s,%s,%s,%s,%s)
        # """
        # print(type(item["article_tags"]),type(item["article_date"]),type(item["url_id"]),type(item["vote_num"]),type(item["cover_url"]))
        # cursor.execute(insert_sql, (item["article_title"], item["article_date"], item["url_id"],
        #               item["vote_num"], item["cover_url"],item["article_tags"]))
        insert_sql,parms = item.get_insert_sql()
        print(insert_sql,parms)
        cursor.execute(insert_sql,parms)

