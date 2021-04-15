from lxml import etree
import re
import json
f = open('item_test.html','r')
html=f.read()
tree = etree.HTML(html)
data={}
title=tree.xpath("//div[@class='summary_info clearfix']/h3")[0].text.strip()
old_title=tree.xpath("//div[@class='summary_info clearfix']/h3/em/@data-content") if tree.xpath("//div[@class='summary_info clearfix']/h3/em/@data-content") else ''
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
print(type(data))
c = open('test_code.csv','w')
new_data = {}
for k,v in data.items():
    #print(repr(k),type(k))
    #print(v,type(v))
    new_data[k.encode('utf8')] = v.encode('utf-8')
print(new_data)
print(json.dumps(data))
#c.write(json.dumps(new_data))
for k in data:
    c.write(k+'\n')
