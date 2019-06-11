# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# This Class define the item crawled from the website, will be used 
# to output the file 
class PlayerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    player_detail = scrapy.Field()
    player_perform = scrapy.Field()
    club_information = scrapy.Field()

