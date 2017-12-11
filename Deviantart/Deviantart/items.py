# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DeviantartItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 图片链接
    img_url = scrapy.Field()

    # 原图链接
    img_bigUrl = scrapy.Field()

    # 图片的标题
    img_title = scrapy.Field()

    # 图片的作者
    img_designer = scrapy.Field()

    # 图片的标签tag
    img_tag = scrapy.Field()

    # 图片的提交时间
    img_time = scrapy.Field()

    # 图片的大小
    # img_size = scrapy.Field()

    # 图片的尺寸,解析度
    img_resolution = scrapy.Field()

    # 图片的浏览数量
    img_watch = scrapy.Field()

    # 图片的喜爱数量
    img_like = scrapy.Field()

    # 图片的评论数量
    img_talk = scrapy.Field()

    # 图片的下载数量
    img_down = scrapy.Field()

    # 图片所属的专辑
    img_set = scrapy.Field()

    # 图片详情页链接
    img_link = scrapy.Field()
