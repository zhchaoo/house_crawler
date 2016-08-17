# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseItem(scrapy.Item):
    # define the fields for your item here like:
    py_id = scrapy.Field()
    zone = scrapy.Field()
    address = scrapy.Field()
    total_price = scrapy.Field()
    area_size = scrapy.Field()
    per_price = scrapy.Field()

