# -*- coding: utf-8 -*-

import csv

class BuptbbsspiderPipeline(object):

    def open_spider(self, spider):
        f = open('./BUPTData/data_' + spider.name + '.csv', 'x', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow(('post_time', 'post_id', 'post_sex', 'post_title', 'reply_id', 'content',
                         'thread_title', 'thread_owner', 'thread_url', 'board_name_cn',
                         'board_name_en'))


    def process_item(self, item, spider):

        f = open('./BUPTData/data_' + spider.name + '.csv', 'a+', encoding='utf-8')
        writer = csv.writer(f)
        writer.writerow((item['post_time'], item['post_id'], item['post_sex'], item['post_title'], item['reply_id'],
                         item['content'], item['thread_title'], item['thread_owner'], item['thread_url'],
                         item['board_name_cn'], item['board_name_en']))
        return item
