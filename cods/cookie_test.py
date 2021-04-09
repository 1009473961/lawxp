import requests
import json
import re
from lxml import etree
reurl = 'https://ss.cods.org.cn/latest/searchR?q=%E7%9F%B3%E5%AE%B6%E5%BA%84%E4%B8%AD%E5%AD%A6&t=common&currentPage=1&scjglx=B'

#url='https://ss.cods.org.cn/latest/detail?jgdm=7bee23e2d245f9c4114f07bfd13f857d'
url='https://ss.cods.org.cn/latest/searchR?q=面包&t=common&currentPage=1&scjglx=B'
head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Cookie':'kefuCookie=fbd0c5f257544623ae2df7cb5008b767; JSESSIONID=8FA02447FC01353269C961FEBD034F98',
        'Host':'ss.cods.org.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'Referer':reurl}
r=requests.get(url,headers=head)
print(r.text)
tree = etree.HTML(r.text)
#详情页测试
'''
data={}
title=tree.xpath("//div[@class='summary_info clearfix']/h3")[0].text.strip()
old_title=tree.xpath("//div[@class='summary_info clearfix']/h3/em/@data-content")
#print(tree.xpath("//div[@class='summary_info clearfix']/ul/li"))
#print(tree.xpath("//div[@class='summary_info clearfix']/ul/li[1]/text()"))
data['title'] = title
data['old_title'] = old_title
for info in tree.xpath("//div[@class='summary_info clearfix']/ul/li"):
    #print(info.xpath('./label')[0].text)
    #print(info.xpath("./text()")[2].strip())
    k = info.xpath('./label')[0].text
    v = info.xpath("./text()")[2].strip()
    data[k] = v
#print(data)
#print(tree.xpath("//div[@class='summary_info clearfix']/h3")[1])
for info in tree.xpath("//div[@class='summary_info clearfix']/h3")[1]:
    data_sum = info.xpath("./text()")
    if data_sum and "：" in data_sum[0]:
        print(data_sum[0])
        k,v = data_sum[0].split('：')
        data[k] = v
print(data)
codes_name=tree.xpath("//div[@class='codes clearfix']/ul/li/h3")[0].text
codes_values=tree.xpath("//div[@class='codes clearfix']/ul/li/p/text()")[0]
data[codes_name] = codes_values
print(data)
#print(tree.xpath("//div[@class='detmain']"))
for half in tree.xpath("//div[@class='detmain']/ul/li"):
    print(half.xpath("./h6")[0].text) if half.xpath("./h6") else ''
    half_k = (half.xpath("./h6")[0].text) if half.xpath("./h6") else ''
    if half.xpath("./p"):
        print(half.xpath("./p/text()"))
        half_v = half.xpath("./p/text()")[0]
    else:
        print(''.join(half.xpath("./text()")).strip())
        half_v = ''.join(half.xpath("./text()")).strip()
    data[half_k] = half_v
print(data)
'''



#列表页测试

for info in tree.xpath("//div[@class='result result-2']/div[@class='each has-img']/div[@class='tit']/a"):
        print(info.xpath("./@title"))
f = open('list_page.html','w')
f.write(r.text)
f.flush()
f.close()



