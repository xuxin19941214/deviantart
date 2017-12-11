# -*- coding: utf-8 -*-
import scrapy
import re
import time
from scrapy.http.request import Request
from Deviantart.items import DeviantartItem


class DeviantartSpider(scrapy.Spider):
    name = 'deviantart'
    allowed_domains = ['deviantart.com']
    start_urls = ['http://deviantart.com/']

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
    }

    # 起始url
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.header, callback=self.parse)

    # 处理大类链接
    def parse(self, response):
        # 各分类链接
        link_lists = response.xpath(
            '//li/a[@class="cat-depth-0"]/@href').extract()[0:1]
        print(link_lists)
        for link_list in link_lists:
            yield Request(url=link_list, headers=self.header, callback=self.parse_middle)
        # 策展库各分类的名字
        # Li_class_name = response.xpath('//h2[@class="rf-curated-galleries-cover__label qa-curated-galleries-cover__label"]/text()').extract()

        # for i, Li_img_link in enumerate(Li_link_list):
        #     # https://www.behance.net/v2/galleries/2/projects?ordinal=48
        #     # https://www.behance.net/galleries/2/Graphic-Design?tracking_source=view-all
        #     item = BehanceItem()
        #     parten = re.compile(r'.*?/galleries/(\d+)/.*')
        #     num1 = parten.findall(Li_img_link)[0]
        #     # item['Li_classes'] = Li_class_name[i]
        #     for i in range(50000 // 48):
        #         ordinal = 0 + i * 48
        #         # 各图片集的链接
        #         Li_img_link = 'https://www.behance.net/v2/galleries/' + num1 + '/projects?ordinal=' + str(ordinal)

                # yield Request(url=Li_img_link, headers=self.second_header, callback=self.Li_jsonData,
                #               meta={'meta_1': item})

    # 提取大类下级类别链接
    def parse_middle(self, response):
        # meta_1 = response.meta['meta_1']
        # data = json.loads(response.body.decode('utf-8'))
        # data_list = data['entities']
        # for data in data_list:
        #     item = BehanceItem()
        #     item['name'] = data['name']
        #     item['designer'] = data['owners'][0]['display_name']
        #     item['setList'] = data['share_url']
        #     item['watch_count'] = data['stats']['views']
        #     item['like_count'] = data['stats']['appreciations']
        #     item['talk_count'] = data['stats']['comments']
        #     # item['img_type'] = data['field_links']['name']
        #     item['img_type'] = ','.join(map(lambda x: x['name'], data['field_links']))
        #     yield Request(url=item['setList'], headers=self.header, callback=self.Li_bottom_parse,
        #                   meta={'meta_1': item})
        link_lists = response.xpath('//li/a[@class="cat-depth-2"]/@href').extract()
        # print(link_lists1)
        for link_list in link_lists:
            yield Request(url=link_list, headers=self.header, callback=self.parse_bottom)
        # for link_list1 in link_lists1:
        #     for i in range(39984 // 24):
        #         offset = 0 + i * 24
        #         link_list1 = link_list1 + '?offset=' + str(offset)
        #         yield Request(url=link_list1, headers=self.header, callback=self.parse_imgLink)

    # 处理下一级分类链接
    def parse_bottom(self, response):
        try:
            link_lists = response.xpath('//li/a[@class="cat-depth-3"]/@href').extract()
            if len(link_lists) > 0:
                print('=======================\\\\\\\\\\\\\\\\')
                print(link_lists)
                print('=======================\\\\\\\\\\\\\\\\')
                for link_list in link_lists:
                    yield Request(url=link_list, headers=self.header, callback=self.parse_next)
            else:
                print('------------------\\\\\\\\\\\\\\\\')
                print(response.url)
                print('------------------\\\\\\\\\\\\\\\\')
                # for i, link_list in enumerate(link_lists):
                for i in range(39984 // 24):
                    offset = 0 + i * 24
                    link_list = response.url + '?offset=' + str(offset)
                    yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)
        except Exception as e:
            print(e)

    # 处理下一级链接
    def parse_next(self, response):
        try:
            link_lists = response.xpath('//li/a[@class="cat-depth-4"]/@href').extract()
            if len(link_lists) > 0:
                print('=======================\\\\\\\\\\\\\\\\')
                print(link_lists)
                print('=======================\\\\\\\\\\\\\\\\')
                for link_list in link_lists:
                    yield Request(url=link_list, headers=self.header, callback=self.parse_nextOne)
            else:
                print('------------------\\\\\\\\\\\\\\\\')
                print(response.url)
                print('------------------\\\\\\\\\\\\\\\\')
                # for i, link_list in enumerate(response.url):
                for i in range(39984 // 24):
                    offset = 0 + i * 24
                    link_list = response.url + '?offset=' + str(offset)
                    yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)
                # yield self.parse_deal(response)
        except Exception as e:
            print(e)

    # 处理最后一级上一级
    def parse_nextOne(self, response):
        try:
            link_lists = response.xpath('//li/a[@class="cat-depth-5"]/@href').extract()
            if len(link_lists) > 0:
                print('=======================\\\\\\\\\\\\\\\\')
                print(link_lists)
                print('=======================\\\\\\\\\\\\\\\\')
                for link_list in link_lists:
                    yield Request(url=link_list, headers=self.header, callback=self.parse_last)
            else:
                print('------------------\\\\\\\\\\\\\\\\')
                print(response.url)
                print('------------------\\\\\\\\\\\\\\\\')
                # for i, link_list in enumerate(response.url):
                for i in range(39984 // 24):
                    offset = 0 + i * 24
                    link_list = response.url + '?offset=' + str(offset)
                    yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)
                # yield self.parse_deal(response)
        except Exception as e:
            print(e)

    # 处理最后一级
    def parse_last(self, response):
        try:
            link_lists = response.xpath('//li/a[@class="cat-depth-6"]/@href').extract()
            if len(link_lists) > 0:
                print('=======================\\\\\\\\\\\\\\\\')
                print(link_lists)
                print('=======================\\\\\\\\\\\\\\\\')
                for k, link_list in enumerate(link_lists):
                    for k in range(39984 // 24):
                        offset = 0 + k * 24
                        link_list = link_list + '?offset=' + str(offset)
                        yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)
            else:
                print('------------------\\\\\\\\\\\\\\\\')
                print(response.url)
                print('------------------\\\\\\\\\\\\\\\\')
                for i in range(39984 // 24):
                    offset = 0 + i * 24
                    link_list = response.url + '?offset=' + str(offset)
                    yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)
        except Exception as e:
            print(e)

    # 处理图片页面
    # def parse_deal(self, response):
    #     for i, link_list in enumerate(link_lists):
    #         for i in range(39984 // 24):
    #             offset = 0 + i * 24
    #             link_list = link_list + '?offset=' + str(offset)
    #             yield Request(url=link_list, headers=self.header, callback=self.parse_imgLink)

    # 提取图片页面链接进行处理图片页面
    def parse_imgLink(self, response):
        img_htmlLinks = response.xpath('//a[@class="torpedo-thumb-link"]/@href').extract()
        for img_htmlLink in img_htmlLinks:
            yield Request(url=img_htmlLink, headers=self.header, callback=self.parse_imgHtml)

    def parse_imgHtml(self, response):
        item = DeviantartItem()
        item['img_link'] = response.url
        # 图片链接
        img_urls = response.xpath('//div[@class="dev-view-deviation"]/img[1]/@src').extract()
        # print(img_urls)
        try:
            # for img_url in img_urls:
            item['img_url'] = img_urls[0]
            # print(item['img_url'])
        except Exception as e:
            item['img_url'] = ''

        # 原图链接
        img_bigUrls = response.xpath('//div[@class="dev-view-deviation"]/img[2]/@src').extract()
        # print(img_bigUrls)
        try:
            # for img_bigUrl in img_bigUrls:
            item['img_bigUrl'] = img_bigUrls[0]
            # print(item['img_bigUrl'])
        except Exception as e:
            item['img_bigUrl'] = ''

        # 图片的标题
        img_titles = response.xpath('//a[@class="title"]/text()').extract()
        try:
            # print(img_titles)
            # for img_title in img_titles:
            item['img_title'] = img_titles[0]
            # print(item['img_title'])
        except Exception as e:
            item['img_title'] = ''

        # 图片的作者
        img_designers = response.xpath('//small[@class="author"]//span[@class="username-with-symbol u"]/a/text()').extract()
        try:
            # print(img_designers)
            # for img_designer in img_designers:
            item['img_designer'] = img_designers[0]
            # print(item['img_designer'])
        except Exception as e:
            item['img_designer'] = ''

        # 图片的标签tag
        img_tag = response.xpath('//span[@class="dev-about-breadcrumb"]//text()').extract()
        try:
            # print(img_tag)
            img_tag = "".join(img_tag)
            # print("=====================")
            # print(img_tag)
            # print("=====================")
            item['img_tag'] = img_tag
        except Exception as e:
            item['img_tag'] = ''

        # 图片的提交时间
        img_times = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-details"]//span/@ts').extract()
        # print(img_times)
        try:
            # 转换成localtime
            img_time = img_times[0]
            # print(img_time)
            time1 = time.localtime(int(img_time))
            # print(time1)
            # 转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time1)
            # print(dt)
            # print(img_times)
            # for img_time in img_times:
            item['img_time'] = dt
            # print(item['img_time'])
        except Exception as e:
            item['img_time'] = ''

        # 图片的大小
        # img_sizes = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-details"]//dd[2]/text()').extract()
        # try:
        #     # print(img_sizes)
        #     # for img_size in img_sizes:
        #     item['img_size'] = img_sizes[0]
        #     # print(item['img_size'])
        # except Exception as e:
        #     item['img_size'] = ''

        # 图片的尺寸,解析度
        img_resolutions = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-details"]//dd[3]/text()').extract()
        try:
            # print(img_resolutions)
            # for img_resolution in img_resolutions:
            item['img_resolution'] = img_resolutions[0]
            # print(item['img_resolution'])
        except Exception as e:
            item['img_resolution'] = ''

        # 图片的浏览数量
        img_watchs = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-stats"]//dd[1]/text()').extract()
        try:
            # print(img_watchs)
            # for img_watch in img_watchs:
            img_watch = img_watchs[0]
            img_watch = ''.join(img_watch.split(','))
            item['img_watch'] = img_watch
            # print(item['img_watch'])
        except Exception as e:
            item['img_watch'] = ''

        # 图片的喜爱数量
        img_likes = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-stats"]//dd[2]/text()[1]').extract()
        # print('....................')
        # print(img_likes)
        # print('....................')
        # img_like = img_likes[0]
        try:
            # for img_like in img_likes:
            img_like = img_likes[0]
            img_like = ''.join(img_like.split(','))
            item['img_like'] = img_like
            # print(item['img_like'])
        except Exception as e:
            item['img_like'] = ''

        # 图片的评论数量
        img_talks = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-stats"]//dd[3]/text()').extract()
        try:
            # print(img_talks)
            # for img_talk in img_talks:
            img_talk = img_talks[0]
            img_talk = ''.join(img_talk.split(','))
            item['img_talk'] = img_talk
            # print(item['img_talk'])
        except Exception as e:
            item['img_talk'] = ''

        # 图片的下载数量
        img_downs = response.xpath('//div[@class="dev-right-bar-content dev-metainfo-content dev-metainfo-stats"]//dd[4]/text()').extract()
        try:
            # for img_down in img_downs:
            img_down = img_downs[0]
            img_down = ''.join(img_down.split(','))
            item['img_down'] = img_down
        except Exception as e:
            item['img_down'] = ''

        # 图片所属的专辑
        img_set = response.xpath('//div[@class="more-from-collection-preview-row"]/h4//text()').extract()
        try:
            # print(img_set)
            img_set = ''.join(img_set)
            # print("===============")
            # print(img_set)
            # print("===============")
            # img_sets = ','.join(map(lambda x: x.strip(), img_sets))
            a = re.compile('\s{2,}')
            img_set = a.sub(',', img_set)
            item['img_set'] = img_set
        except Exception as e:
            item['img_set'] = ''

        yield item
