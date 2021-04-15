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
db=pymongo.MongoClient('127.0.0.1').admin
INFO=logging.info
ERROR=logging.error

class Code_Spider(scrapy.Spider):
    name='code_word'
    cus_retry_times = 5
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
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'kefuCookie=fbd0c5f257544623ae2df7cb5008b767; JSESSIONID=8FA02447FC01353269C961FEBD034F98',
            'Host': 'ss.cods.org.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
            }
        #cook = {"kefuCookie": 'fbd0c5f257544623ae2df7cb5008b767', 'JSESSIONID': '8FA02447FC01353269C961FEBD034F98'}
        #jsessionid_list = [x['jsessionid'] for x in db.user_cookie.find({'state':'available'})]
        jsessionid_list = [x['jsessionid'] for x in db.user_cookie.find({'mobile': '13301242741'})]
        cook = {'JSESSIONID':random.choice(jsessionid_list)}
        return head,cook
    def start_requests(self):
        start=0

        for end in range(start,101,100):
            if not end:
                continue
            print(start,end)
            url='https://fapi.lawxp.com/v1/CkeyWord?startid=%s&endid=%s'%(start,end)
            #time.sleep(5)
            #print('start_requests'+url)
            INFO('关键词接口 起始数 %s,结束数 %s, 链接 %s'%(start,end,url))
            start=end
            yield Request(url,callback=self.get_word)

        #head,cook = self.cooke_head()
        #url = 'https://ss.cods.org.cn/latest/detail?jgdm=8c18ba47fa75baf40befda902b482251'

        #yield Request(url,headers=head,cookies=cook,callback=self.item_parse)
    def get_word(self,response):
        data=json.loads(response.text)
        for word_data in data['data']:
            #print(word_data['companyName'])
            word = word_data['companyName']
            #word='面包'
            word_url = 'https://ss.cods.org.cn/latest/searchR?q=%s&t=common&currentPage=1&scjglx=B'%word
            referer='https://ss.cods.org.cn/latest/searchR?q=%s&currentPage=1&t=common&searchToken='%word
            #print(repr(word_url))
            head,cook =self.cooke_head()
            head['Referer'] = referer
            #time.sleep(5)
            INFO('%s %s %s %s'%(response.url,word,cook,'page=1'))
            yield Request(word_url,headers=head,callback=self.parse,cookies=cook,meta={'page':1,'word':word,'word_url':response.url})
    def parse(self,response):
        #print(response.text)
        #print(response.headers)
        #print(response.request)
        #print(response.request.headers)
        #if not self.verify_cook(response.request.cookie['JSESSIONID'],response.text):
        verify = self.verify_cook(response.request.cookies['JSESSIONID'],response.text)
        if verify != True:
            ERROR('cookies：%s,链接:%s,关键词:%s,页数:%s Error :%s,retry:%s'%(response.request.cookies['JSESSIONID'],response.url,response.meta['word'],response.meta['page'],verify,response.meta.get('cus_retry_times', 0)))
            self.crawler.engine.close_spider(self,'verify fail error %s %s'%(response.request.cookies['JSESSIONID'],verify))
            #raise Exception(verify)
            retries = response.meta.get('cus_retry_times', 0) + 1
            if retries <= self.cus_retry_times:
                r = response.request.copy()
                r.meta['cus_retry_times'] = retries
                r.dont_filter = True
                time.sleep(2)
                head,cook = self.cooke_head()
                yield r
            else:
                #self.logger.debug("Gave up retrying {}, failed {} times".format(response.url, retries))
                ERROR('max retry %s %s'%(response.url,retries))

        list_word = AllCodsList()
        list_word['word'] = response.meta['word']
        list_word['url'] = response.meta['word_url']
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
            yield Request(title_url,headers=head,cookies=cook,callback=self.item_parse,meta={'word':response.meta['word']})
        all_items = response.xpath("//div[@class='position position2']/p/strong/text()").extract()
        if all_items:
            item_num = all_items[0].replace(',','')
            page = response.meta['page']
            if page * 10 < int(item_num) and page < 10:
                next_page = page + 1
                wordurl = response.url
                next_url = wordurl.replace('currentPage=%s'%page,'currentPage=%s'%next_page)
                head, cook = self.cooke_head()
                INFO('word_page_next word:%s,page:%s,all_page:%s,next_page:%s，cookie:%s'%(response.meta['word'],page,int(item_num)/10,next_page,cook))
                time.sleep(2)
                yield Request(next_url,headers=head,callback=self.parse,cookies=cook,meta={'page':next_page,'word':response.meta['word'],'word_url':response.meta['word_url']})
    def item_parse(self,response):
        item = AllCodsItem()
        data = {}
        INFO('Item url : %s cookie : %s word : %s ' % (response.url, response.request.cookies['JSESSIONID'], response.meta['word']))
        verify = self.verify_cook(response.request.cookies['JSESSIONID'], response.text)
        if verify != True:
            ERROR('cookies:%s,详情页链接:%s,关键词:%s Error:%s retry:%s' % (response.request.cookies['JSESSIONID'], response.url, response.meta['word'], verify,response.meta.get('cus_retry_times', 0)))
            self.crawler.engine.close_spider(self, 'verify fail error %s %s' % (response.request.cookies['JSESSIONID'], verify))
            retries = response.meta.get('cus_retry_times', 0) + 1
            if retries <= self.cus_retry_times:
                r = response.request.copy()
                r.meta['cus_retry_times'] = retries
                r.dont_filter = True
                time.sleep(2)
                head, cook = self.cooke_head()
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