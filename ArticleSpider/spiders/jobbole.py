# -*- coding: utf-8 -*-
import scrapy

class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/110916/']

    def parse(self, response):
        # req_urls = response.css('#archive .floated-thumb .post-meta a::attr(href)').extract()
        # for req_url in req_urls:
        #    yield req_url
        self.content_parse(response)


    def content_parse(self,response):
        # response.xpath('//*[@id="post-110916"]/div[1]/h1/text()').extract_first('');
        article_title = response.css('.entry-header h1::text').extract_first('')
        # response.xpath('//*[@id="post-110916"]/div[2]/p/text()').extract_first('').strip().replace(' ·', '');
        article_date = response.css('.entry-meta-hide-on-mobile::text').extract_first('').strip().replace(' ·', '')
        # tags
        article_tags = response.css('.entry-meta-hide-on-mobile a::text').extract()
        vote_num = int(response.css('.vote-post-up h10::text').extract_first('0'))
        print("article_title:",article_title,"article_date:",article_date,"article_tags:",article_tags,"vote_num:",vote_num)
        pass