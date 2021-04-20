# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
import json
from scrapy.http import Request
from all_cods.items import AllCodsItem,AllCodsList
import time
import pymongo
import random
import logging
import datetime
from scrapy_redis.spiders import RedisSpider
from ..ua_list import agents
import urllib
db=pymongo.MongoClient('127.0.0.1').admin
INFO=logging.info
ERROR=logging.error

class Code_Spider(RedisSpider):
    name='redis_code_word'
    cus_retry_times = 5
    redis_key = 'redis_code_word:start_urls'
    def verify_cook(self,cookie,text):
        print(cookie)
        if '系统将暂停为您提供服务' in text:
            db.user_cookie.update_one({'jsessionid':cookie},{'$set':{'state':'frequently','datetime':datetime.datetime.now()}})
            return 'frequently'
        elif '认证已失效' in text:
            db.user_cookie.update_one({'jsessionid': cookie}, {'$set': {'state': 'login_again'}})
            return 'login_again'
        else:
            return True

    def cooke_head(self):
        head = {
            'User-Agent': random.choice(agents),
            }

        #cook = {"kefuCookie": 'fbd0c5f257544623ae2df7cb5008b767', 'JSESSIONID': '8FA02447FC01353269C961FEBD034F98'}
        #jsessionid_list = [x['jsessionid'] for x in db.user_cookie.find({'state':'available'})]
        jsessionid_list = [x['jsessionid'] for x in db.user_cookie.find({'mobile': '13301242741'})]
        cook = {'JSESSIONID':random.choice(jsessionid_list)}
        return head,cook
    def parse(self,response):
        print(response.url)
        verify = self.verify_cook(response.request.cookies['JSESSIONID'],response.text)
        word_url = re.findall("q=(.*?)&",response.url)[0]
        word = urllib.request.unquote(word_url)
        INFO('关键词 %s, 页数 %s, cookies:%s,ua:%s'%(word,response.meta.get('page',1),response.request.cookies['JSESSIONID'],response.request.headers['User-Agent']))
        print(word)
        if verify != True:
            ERROR('cookies：%s,链接:%s,关键词:%s,页数:%s Error :%s,retry:%s'%(response.request.cookies['JSESSIONID'],response.url,response.meta['word'],response.meta['page'],verify,response.meta.get('cus_retry_times', 0)))
            self.crawler.engine.close_spider(self,'verify fail list error %s %s'%(response.request.cookies['JSESSIONID'],verify))
            #raise Exception(verify)
            retries = response.meta.get('cus_retry_times', 0) + 1
            if retries <= self.cus_retry_times:
                r = response.request.copy()
                r.meta['cus_retry_times'] = retries
                r.dont_filter = True
                time.sleep(2)
                head,cook = self.cooke_head()
                r.cookies = cook
                yield r
            else:
                #self.logger.debug("Gave up retrying {}, failed {} times".format(response.url, retries))
                ERROR('max retry %s %s'%(response.url,retries))

        list_word = AllCodsList()
        list_word['word'] = word
        list_word['url'] = response.url
        if '检索词范围过大' in response.text:
            type_word = '检索词范围过大'
            list_word['type_word'] = type_word
            yield list_word
        elif '暂无搜索数据' in response.text:
            type_word = '暂无搜索数据'
            list_word['type_word'] = type_word
            yield list_word
        for line in response.xpath("//div[@class='result result-2']/div[@class='each has-img']/div[@class='tit']/a"):
            title_url = 'https://ss.cods.org.cn' + line.xpath("./@title").extract()[0]
            print(title_url)
            #time.sleep(10)
            head, cook = self.cooke_head()
            time.sleep(2)
            yield Request(title_url,headers=head,cookies=cook,callback=self.item_parse,meta={'word':word})
        all_items = response.xpath("//div[@class='position position2']/p/strong/text()").extract()
        if all_items:
            item_num = all_items[0].replace(',','')
            page = response.meta.get('page',1)
            if page * 10 < int(item_num) and page < 10:
                next_page = page + 1
                wordurl = response.url
                next_url = wordurl.replace('currentPage=%s'%page,'currentPage=%s'%next_page)
                head, cook = self.cooke_head()
                INFO('word_page_next word:%s,page:%s,all_page:%s,next_page:%s，cookie:%s'%(word,page,int(item_num)/10,next_page,cook))
                time.sleep(2)
                yield Request(next_url,headers=head,callback=self.parse,cookies=cook,meta={'page':next_page,'word':word})
    def item_parse(self,response):
        item = AllCodsItem()
        data = {}
        INFO('Item url : %s cookie : %s word : %s ' % (response.url, response.request.cookies['JSESSIONID'], response.meta['word']))
        verify = self.verify_cook(response.request.cookies['JSESSIONID'], response.text)
        if verify != True:
            ERROR('cookies:%s,详情页链接:%s,关键词:%s Error:%s retry:%s' % (response.request.cookies['JSESSIONID'], response.url, response.meta['word'], verify,response.meta.get('cus_retry_times', 0)))
            self.crawler.engine.close_spider(self, 'verify fail item error %s %s' % (response.request.cookies['JSESSIONID'], verify))
            retries = response.meta.get('cus_retry_times', 0) + 1
            if retries <= self.cus_retry_times:
                r = response.request.copy()
                r.meta['cus_retry_times'] = retries
                r.dont_filter = True
                time.sleep(2)
                head, cook = self.cooke_head()
                r.cookies= cook
                yield r
            else:
                # self.logger.debug("Gave up retrying {}, failed {} times".format(response.url, retries))
                ERROR('max retry %s %s' % (response.url, retries))
                raise('max retry %s'%verify)

        title = response.xpath("//div[@class='summary_info clearfix']/h3[1]/text()").extract()[0].strip()
        # try:
        #     title = response.xpath("//div[@class='summary_info clearfix']/h3[1]/text()").extract()[0].strip()
        # except:
        #     url = response.url
        #     jgdm=re.findall("jgdm=(.*)",response.url)
        #     f = open('error_item_%s.html'%jgdm,'w')
        #     f.write(response.text)
        #     f.flush()
        #     f.close()
        #print(title)
        old_title = response.xpath("//div[@class='summary_info clearfix']/h3/em/@data-content/text()").extract()
        data['title'] = title
        data['old_title'] = old_title[0] if old_title else ''
        data['word'] = response.meta['word']
        for info in response.xpath("//div[@class='summary_info clearfix']/ul/li"):
            k = info.xpath('./label/text()').extract()[0]
            v = info.xpath("./text()").extract()[2].strip()
            data[k] = v
        #print(data)
        for info in response.xpath("//div[@class='summary_info clearfix']/h3[2]/em/text()"):
            data_sum = info.extract()
            # print(data_sum)
            # exit()
            if data_sum and "：" in data_sum:
                k, v = data_sum.split('：')
                data[k] = v
        codes_name = response.xpath("//div[@class='codes clearfix']/ul/li/h3/text()").extract()[0].strip()
        codes_values = response.xpath("//div[@class='codes clearfix']/ul/li/p/text()").extract()[0]
        #print(codes_values)
        data[codes_name] = codes_values
        for half in response.xpath("//div[@class='detmain']/ul/li"):
            #print(half.xpath("./h6/text()").extract()[0]) if half.xpath("./h6/text()") else ''
            half_k = (half.xpath("./h6/text()").extract()[0]) if half.xpath("./h6/text()") else ''
            if half.xpath("./p"):
                #print(half.xpath("./p/text()").extract()[0])
                half_v = half.xpath("./p/text()").extract()[0] if half.xpath("./p/text()").extract() else ''
            else:
                #print(''.join(half.xpath("./text()").extract()).strip())
                half_v = ''.join(half.xpath("./text()").extract()).strip()
            data[half_k] = half_v
        #print(data)
        #print(data['统一社会信用代码'])
        item['data']=data
        #yield item

        jgdm=re.findall("jgdm=(.*)",response.url)
        history_url = 'https://ss.cods.org.cn/latest/getOtherInfo?jgdm=%s'%jgdm[0]
        head,cook=self.cooke_head()
        #print(history_url)
        yield Request(history_url,headers=head,cookies=cook,callback=self.history_parse,meta={'item_item':item})

    def history_parse(self,response):
        item=response.meta['item_item']
        data = json.loads(response.text)
        item['history'] = data['historyList']
        #print(data)
        yield item