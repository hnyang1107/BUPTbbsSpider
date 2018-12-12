# -*- coding: utf-8 -*-
import scrapy
import re
from BUPTbbsSpider.items import BuptbbsspiderItem
from scrapy.http import Request
from scrapy.loader.processors import Join

class BuptS6Spider(scrapy.Spider):
    name = 'bupt_s6'
    allowed_domains = ['bbs.cloud.icybee.cn']
    start_urls = ['http://bbs.cloud.icybee.cn/section/6/']

    def parse(self, response):

        boards = response.xpath('//table/tbody/tr/td[contains(@class,"title_1")]')
        items_1 = []

        for board in boards:

            # 不包含section的信息
            if board.xpath('a/@href').re('/(.*)/')[0] == 'board':

                item = BuptbbsspiderItem()

                item['board_url'] = 'http://bbs.cloud.icybee.cn' + board.xpath('a/@href').extract()[0]
                item['board_name_cn'] = board.xpath('a/text()').extract()[0]
                item['board_name_en'] = board.xpath('text()').extract()[0]

                items_1.append(item)
        for item in items_1:
            yield Request(url=item['board_url'], meta={'item_1': item}, callback=self.parse_item)

    # 增加页数
    def parse_item(self, response):

        item_1 = response.meta['item_1']
        items = []
        board_url_index = response.url

        try:
            num_pages = int(response.xpath('//div[@class="page"]/ul/li[2]//li[position()=last()-1]/a/text()').extract()[0])
        except:
            num_pages = 1

        for page in range(1, num_pages + 1):

            item = item_1.copy()
            item['thread_page_url'] = board_url_index + '?p=' + str(page)

            items.append(item)

        for item in items:
            yield Request(url=item['thread_page_url'], meta={'item_2': item}, callback=self.parse_detail)


    def parse_detail(self, response):

        item_2 = response.meta['item_2']
        items = []

        threads = response.xpath('//tbody//tr')

        for thread in threads:
            item = item_2.copy()
            item['thread_title'] = thread.xpath('td[contains(@class,"title_9")]/a/text()').extract()[0]
            item['thread_url'] = 'http://bbs.cloud.icybee.cn' + thread.xpath('td[contains(@class,"title_9")]/a/@href').extract()[0]
            item['thread_owner'] = thread.xpath('td[contains(@class,"title_12")][1]/a/text()').extract()[0]
            items.append(item)
        for item in items:
            yield Request(url=item['thread_url'], meta={'item_3': item}, callback=self.parse_detail_2)

    # 帖子有很多页
    def parse_detail_2(self, response):

        item_3 = response.meta['item_3']
        items = []

        try:
            num_pages = int(response.xpath('//div[@class="page"]/ul/li[2]//li[position()=last()-1]/a/text()').extract()[0])
        except:
            num_pages = 1

        for page in range(1, num_pages + 1):

            item = item_3.copy()
            item['post_url'] = response.url + '?p=' + str(page)

            items.append(item)

        for item in items:
            yield Request(url=item['post_url'], meta={'item_4': item}, callback=self.parse_detail_3)


    def parse_detail_3(self, response):

        item_4 = response.meta['item_4']

        post_cards = response.xpath('//div[@class="a-wrap corner"]')

        for post_card in post_cards:
            item = item_4.copy()

            item['post_id'] = post_card.xpath('table//span[@class="a-u-name"]//text()').extract()[0]

            try:
                item['post_sex'] =  post_card.xpath('table//span[@class="a-u-sex"]//@title').re('(.*)哦')[0]
            except:
                item['post_sex'] = '性别保密'

            item['post_title'] = post_card.xpath('table//div[@class="a-content-wrap"]//text()').re('标\xa0\xa0题:(.*)')[0]
            # item['post_time'] = post_card.xpath('table//div[@class="a-content-wrap"]//text()').re('北邮人论坛 \((.*)\)')[0]
            try:
                item['post_time'] = post_card.xpath('table//div[@class="a-content-wrap"]//text()').re('北邮人论坛 \((.*)\)')[0]
            except:
                item['post_time'] = post_card.xpath('table//div[@class="a-content-wrap"]//text()').re('北邮人论坛站 \((.*)\)')[0]

            content = Join()(post_card.xpath('table//div[@class="a-content-wrap"]/text()[position()>3]').extract())
            try:
                item['reply_id'] = re.findall(r'【 在 (.*?) 的大作中提到: 】', content)[0]
                if '(' in item['reply_id']:
                    item['reply_id'] = re.search(r'(.*) \(', item['reply_id']).group(1)
            except:
                item['reply_id'] = ''

            if re.search(r'(.*) 【', content):
                item['content'] = re.search(r'(.*) 【', content).group(1)
            elif re.search(r' 】 (.*) --', content):
                item['content']= re.search(r' 】 (.*) --', content).group(1)
            elif re.search(r'(.*) --', content):
                item['content'] = re.search(r'(.*) --', content).group(1)
            elif re.search(r'(.*) --', content) == None:
                item['content'] = ''

            yield item
