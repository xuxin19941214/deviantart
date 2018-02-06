# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class Dribbble1Pipeline(object):
#     def process_item(self, item, spider):
#         return item

import pymysql
from scrapy.conf import settings

from scrapy.exceptions import DropItem
from Deviantart.settings import Redis
from qiniu import Auth
from qiniu import BucketManager
import random
import time
import hashlib
import re
import uuid
import requests
import json

# 去重


# class DuplicatesPipeline(object):
#
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self, item, spider):
#         if item['img_url'] in self.ids_seen:
#             raise DropItem("Duplicate item found: %s" % item)
#         else:
#             self.ids_seen.add(item['img_url'])
#             return item
# redis去重


class DuplicatesPipeline(object):
    def process_item(self, item, spider):
        if Redis.exists('url:%s' % item['img_url']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            Redis.set('url:%s' % item['img_url'], 1)
            return item

# 下面是将爬取到的信息插入到MySQL数据库中


class DeviantartPipeline(object):
    def process_item(self, item, spider):
        access_key = ''
        secret_key = ''
        bucket_name = ''
        q = Auth(access_key, secret_key)
        bucket = BucketManager(q)
        # if len(item["img_bigUrl"]) > 0:
        url = item["img_bigUrl"]
        # url = ''
        m = str(random.randint(1, 10)) + str(int(time.time()))
        m = hashlib.md5(m.encode("utf8")).hexdigest()[0:10]
        m = re.sub(r"(?<=\w)(?=(?:\w\w)+$)", "/", m)
        uid = str(uuid.uuid3(uuid.NAMESPACE_DNS, 'url'))
        lastStr = url.rsplit('.', 1)[1]
        key = m + '/' + uid + '.' + lastStr
        ret, info = bucket.fetch(url, bucket_name, key)
        print(info)
        assert ret['key'] == key
        
        host = settings['MYSQL_HOST']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWD']
        db = settings['MYSQL_DBNAME']
        c = settings['CHARSET']
        port = settings['MYSQL_PORT']
        # 数据库连接
        con = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c, port=port)
        # 数据库游标
        cue = con.cursor()
        print("mysql connect succes")  # 测试语句，这在程序执行时非常有效的理解程序是否执行到这一步
       
        try:
            
            print("insert into deviantart_img1 (img_url,img_link,img_bigUrl,img_title,img_designer,img_tag,img_time,img_key,img_resolution,img_watch,img_like,img_talk,img_down,img_set) values({},{},{},{},{},{},{},{},{},{},{},{},{},{},)".format(
                item["img_url"], item["img_link"], item["img_bigUrl"], item["img_title"], item["img_designer"], item["img_tag"], item["img_time"], key, item["img_resolution"], item["img_watch"], item["img_like"], item["img_talk"], item["img_down"], item["img_set"]))
            cue.execute("insert into deviantart_img1 (img_url,img_link,img_bigUrl,img_title,img_designer,img_tag,img_time,img_key,img_resolution,img_watch,img_like,img_talk,img_down,img_set) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                        (item["img_url"], item["img_link"], item["img_bigUrl"], item["img_title"], item["img_designer"], item["img_tag"], item["img_time"], key, item["img_resolution"], item["img_watch"], item["img_like"], item["img_talk"], item["img_down"], item["img_set"]))

            # cue.execute("insert into behance_picSet (design_name,set_name,set_url,set_tag,set_info) values(%s,%s,%s,%s,%s)",
            #             (item['designer'], item['name'], item['setList'], item['img_tags'], item['img_info']))

            # 测试语句
            print("insert success")
        except Exception as e:
            print('Insert error:', e)
            con.rollback()  # 回滚
        else:
            con.commit()  # 提交
        con.close()  # 关闭
        return item
