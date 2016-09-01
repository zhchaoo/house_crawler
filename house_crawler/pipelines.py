# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
import os

from scrapy.exceptions import DropItem


class HouseCrawlerPipeline(object):
    def process_item(self, item, spider):
        if item['total_price']:
            return item
        else:
            raise DropItem("Missing price info %s" % item)


class SQLitePipeline(object):
    database_path = ''
    database_dir = ''
    conn = None

    def __init__(self, database_dir, database_name, logger):
        self.database_dir = database_dir
        self.database_path = os.path.join(database_dir, database_name + ".db")
        self.logger = logger
        print self.database_path
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database_dir=crawler.spider.database_dir,
            database_name=crawler.spider.name,
            logger=crawler.spider.logger
        )

    def open_spider(self, spider):
        if not os.path.exists(self.database_dir):
            os.makedirs(self.database_dir)

        if os.path.exists(self.database_path):
            self.conn = sqlite3.connect(self.database_path)
        else:
            self.create_table()
        self.conn.execute("PRAGMA journal_mode=WAL;")
        self.conn.commit()

    def close_spider(self, spider):
        if self.conn is not None:
            self.conn.commit()
            self.conn.close()
            self.conn = None

    def process_item(self, item, spider):
        try:
            self.conn.execute('insert into houses(id, zone, address, price, size, date) values(?, ?, ?, ?, ?, ?)',
                              (item['py_id'], item['zone'], item['address'],
                               item['total_price'], item['area_size'], item['date'])
                              )
            self.conn.commit()
            self.logger.info("Inserted into database");
        except sqlite3.IntegrityError:
            self.logger.info("Duplicated");
        return item

    def create_table(self):
        self.conn = sqlite3.connect(self.database_path)
        self.conn.execute("create table houses( \
                id integer primary key, \
                zone varchar(20), \
                address varchar(80), \
                price double, \
                size double, \
                date date)"
                          )
        self.conn.commit()
