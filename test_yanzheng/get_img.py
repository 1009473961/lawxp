import requests
import json
import random


head = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': 'ss.cods.org.cn'}

for i in range(10):
    w = random.random()
    url = 'https://www.icris.cr.gov.hk/csci/shwcaptcha.do?checkPoint=login&rand=%s'%w
    print(url)
    r = requests.get(url,headers = head)
    f = open('test_range_%s.png'%i,'wb')
    f.write(r.content)
    f.close()
