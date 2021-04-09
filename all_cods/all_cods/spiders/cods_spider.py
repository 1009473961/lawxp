# -*- coding: utf-8 -*-
import scrapy
import re
import pdb
import json
from scrapy.http import Request
from all_cods.items import AllCodsItem
import time

class Code_Spider(scrapy.Spider):
    name='code_word'
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
        cook = {"kefuCookie": 'fbd0c5f257544623ae2df7cb5008b767', 'JSESSIONID': '8FA02447FC01353269C961FEBD034F98'}
        return head,cook
    def start_requests(self):
        start=0
        '''
        for end in range(3,6,3):
            print(start,end)
            url='https://fapi.lawxp.com/v1/CkeyWord?startid=%s&endid=%s'%(start,end)
            start=end
            #time.sleep(5)
            print('start_requests'+url)
            yield Request(url,callback=self.get_word)
        '''
        head,cook = self.cooke_head()
        url = 'https://ss.cods.org.cn/latest/detail?jgdm=8c18ba47fa75baf40befda902b482251'
        yield Request(url,headers=head,cookies=cook,callback=self.item_parse)
    def get_word(self,response):
        data=json.loads(response.text)
        for word_data in data['data']:
            print(word_data['companyName'])
            word = word_data['companyName']
            word='面包'
            word_url = 'https://ss.cods.org.cn/latest/searchR?q=%s&t=common&currentPage=1&scjglx=B'%word
            referer='https://ss.cods.org.cn/latest/searchR?q=%s&currentPage=1&t=common&searchToken='%word

            print(repr(word_url))
            head,cook =self.cooke_head()
            head['Referer'] = referer
            time.sleep(5)
            yield Request(word_url,headers=head,callback=self.parse,cookies=cook)
    def parse(self,response):
        #print(response.text)
        print(response.headers)
        print(response.request)
        print(response.request.headers)
        head, cook = self.cooke_head()

        for line in response.xpath("//div[@class='result result-2']/div[@class='each has-img']/div[@class='tit']/a"):
            title_url = 'https://ss.cods.org.cn' + line.xpath("./@title").extract()[0]
            print(title_url)
            time.sleep(10)
            yield Request(title_url,headers=head,cookies=cook,callback=self.item_parse)
    def item_parse(self,response):
        item = AllCodsItem()
        data = {}
        title = response.xpath("//div[@class='summary_info clearfix']/h3[1]/text()").extract()[0].strip()
        print(title)

        old_title = response.xpath("//div[@class='summary_info clearfix']/h3/em/@data-content/text()").extract()
        data['title'] = title
        data['old_title'] = old_title[0] if old_title else ''
        for info in response.xpath("//div[@class='summary_info clearfix']/ul/li"):
            k = info.xpath('./label/text()').extract()[0]
            v = info.xpath("./text()").extract()[2].strip()
            data[k] = v
        print(data)
        for info in response.xpath("//div[@class='summary_info clearfix']/h3[2]/em/text()"):
            data_sum = info.extract()
            # print(data_sum)
            # exit()
            if data_sum and "：" in data_sum:
                k, v = data_sum.split('：')
                data[k] = v
        codes_name = response.xpath("//div[@class='codes clearfix']/ul/li/h3/text()").extract()[0].strip()
        codes_values = response.xpath("//div[@class='codes clearfix']/ul/li/p/text()").extract()[0]
        print(codes_values)
        data[codes_name] = codes_values
        for half in response.xpath("//div[@class='detmain']/ul/li"):
            print(half.xpath("./h6/text()").extract()[0]) if half.xpath("./h6/text()") else ''
            half_k = (half.xpath("./h6/text()").extract()[0]) if half.xpath("./h6/text()") else ''
            if half.xpath("./p"):
                print(half.xpath("./p/text()").extract()[0])
                half_v = half.xpath("./p/text()").extract()[0]
            else:
                print(''.join(half.xpath("./text()").extract()).strip())
                half_v = ''.join(half.xpath("./text()").extract()).strip()
            data[half_k] = half_v
        print(data)
        print(data['统一社会信用代码'])
        item['data']=data
        #yield item

        jgdm=re.findall("jgdm=(.*)",response.url)
        history_url = 'https://ss.cods.org.cn/latest/getOtherInfo?jgdm=%s'%jgdm[0]
        head,cook=self.cooke_head()
        print(history_url)
        yield Request(history_url,headers=head,cookies=cook,callback=self.history_parse,meta={'item_item':item})

    def history_parse(self,response):
        item=response.meta['item_item']
        data = json.loads(response.text)
        item['history'] = data['historyList']
        print(data)
        yield item