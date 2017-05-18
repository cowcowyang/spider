# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


# date converter
def date_processor(value):
    try:
        article_date = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        article_date = datetime.datetime.now().date()
    return article_date


# remove comment in tags
def remove_comment(value):
    if "评论" in value:
        return ""
    else:
        return value


# return origin value
def return_value(value):
    return value


class ArticleItemLoader(ItemLoader):
    # 自定义ItemLoader
    default_output_processor = TakeFirst()


class JobboleArticleItem(scrapy.Item):
    # Field(input_processor) item预处理 MapCompose函数处理
    article_title = scrapy.Field()
    article_date = scrapy.Field(
        input_processor=MapCompose(date_processor),
        output_processor=TakeFirst()
    )
    article_tags = scrapy.Field(
        input_processor=MapCompose(remove_comment),
        output_processor=Join(",")
    )
    cover_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    vote_num = scrapy.Field()
    cover_local_path = scrapy.Field()
    url_id = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            insert into article (article_title,article_date,url_id,vote_num,cover_url,article_tags)
            values(%s,%s,%s,%s,%s,%s)
        """

        first_cover_url = ""
        if self["cover_url"]:
            first_cover_url = self["cover_url"][0]
        parms = (self["article_title"], self["article_date"], self["url_id"], self["vote_num"], first_cover_url,
                 self["article_tags"])
        return insert_sql, parms
