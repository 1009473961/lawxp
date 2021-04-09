from scrapy.selector import Selector
from scrapy.http import HtmlResponse
f = open('item.html','r')
html = f.read()
response= Selector(text=html)
data={}
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
    #print(data_sum)
    #exit()
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