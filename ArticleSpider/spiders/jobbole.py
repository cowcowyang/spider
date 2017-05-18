# -*- coding: utf-8 -*-
import scrapy
import datetime
from scrapy.http import Request
from urllib import parse

from ArticleSpider.items import JobboleArticleItem,ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # req_urls = response.css('#archive .floated-thumb .post-meta a::attr(href)').extract()
        req_nodes = response.css('#archive .floated-thumb')
        for req_node in req_nodes:
            req_url = req_node.css('.post-meta a::attr(href)').extract_first()
            img_url = req_node.css('.post-thumb a img::attr(src)').extract_first()
            yield Request(url= parse.urljoin(response.url,req_url) ,meta={"cover_url":img_url},callback=self.parse_detail)
        next_url = response.css('.next.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)


    def parse_detail(self, response):
        # # response.xpath('//*[@id="post-110916"]/div[1]/h1/text()').extract_first('');
        # article_title = response.css('.entry-header h1::text').extract_first('')
        # # response.xpath('//*[@id="post-110916"]/div[2]/p/text()').extract_first('').strip().replace(' ·', '');
        # article_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('').strip().replace(' ·', '')
        # # tags
        # article_tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        # vote_num = int(response.css('.vote-post-up h10::text').extract_first('0'))
        #
        # # print("article_title:", article_title,type(article_title), "article_date:", article_date,type(article_date), "article_tags:", article_tags,type(article_tags),
        # #       "vote_num:", vote_num,type(vote_num),"cover_url:",cover_url,type(cover_url))
        # article_item = JobboleArticleItem()
        # article_item["url_id"] = get_md5(response.url)
        # article_item["article_title"] = article_title
        # try:
        #     article_date = datetime.datetime.strptime(datetime,"%Y/%m/%d").date()
        # except Exception as e:
        #     article_date = datetime.datetime.now().date()
        # article_item["article_date"] = article_date
        # # article_tags = [x.encode('utf-8') for x in article_tags]
        # article_item["article_tags"] = ''.join(article_tags)
        # article_item["vote_num"] = vote_num
        # article_item["cover_url"] = ''.join(cover_url)

        # scrapy item loader
        cover_url = response.meta.get("cover_url")
        item_loader = ArticleItemLoader(item=JobboleArticleItem(),response=response)
        item_loader.add_css('article_title', '.entry-header h1::text')
        item_loader.add_css('article_date', '.entry-meta-hide-on-mobile::text')
        item_loader.add_css('vote_num', '.vote-post-up h10::text')
        item_loader.add_value('cover_url', [cover_url])
        item_loader.add_value('url_id', get_md5(response.url))
        item_loader.add_css('article_tags', '.entry-meta-hide-on-mobile a::text')

        article_item = item_loader.load_item()

        yield article_item