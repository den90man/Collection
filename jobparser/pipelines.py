# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

# from pprint import pprint

import scrapy
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

from scrapy.pipelines.images import ImagesPipeline


class LeroyParserPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.leraoy

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        # collection.drop()
        item['specs'] = self.process_specs(item['specs'])
        try:
            collection.update_one({'link': item['link']}, {'$set': item}, upsert=True)
        except DuplicateKeyError as e:
            print(e, item['link'])
        return item

    @staticmethod
    def process_specs(raw_list):
        specs_dict = dict(zip(raw_list[::2], raw_list[1::2]))

        return specs_dict


class LeroyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [i[1] for i in results if i[0]]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        img_name = str(request.url).split('/')[-1].strip('.jpg')
        product_id = str(item['link']).split('/')[-2].split('-')[-1]
        return f'full/{product_id}/{img_name}.jpg'

