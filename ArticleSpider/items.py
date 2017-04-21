# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class JobboleArticleItem(scrapy.Item):
    article_title = scrapy.Field()
    article_date = scrapy.Field()
    article_tags = scrapy.Field()
    vote_num = scrapy.Field()
    cover_url = scrapy.Field()
    cover_local_path = scrapy.Field()
    url_id = scrapy.Field()
