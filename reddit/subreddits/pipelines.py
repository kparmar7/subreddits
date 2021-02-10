# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class SubredditsPipeline:
    def __init__(self):
        self.createConnection()
        self.createTable()

    def createConnection(self):
        self.conn = sqlite3.connect('sqlite3.db')
        self.curr = self.conn.cursor()

    def createTable(self):
        self.curr.execute("""DROP TABLE IF EXISTS subreddits """)
        self.curr.execute("""create table subreddits(title text,comment text)""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into subreddits values(?,?)""", (
            item["iTitle"][0],
            item["iComment"],
        )
        )
        self.conn.commit()
