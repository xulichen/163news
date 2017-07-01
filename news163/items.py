# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class News163Item(Item):
    title = Field()
    contents = Field()
    post_time = Field()
    post_source = Field()
    ep_editor = Field()
    category = Field()
    # post_comment_tiecount = Field()
    # post_comment_joincount = Field()
