import time
import requests
import sys
import json
from threading import Thread
url='https://www.cods.org.cn/cods/ajax/invoke'
t=int(time.time()*1000)
print(t)
param={'_ZVING_METHOD':'Gee/tartCaptcha?t=%s'%t,'_ZVING_URL':'%2Fcods%2Fmember%2Flogin','_ZVING_DATA':'{}','_ZVING_DATA_FORMAT':'json'}
print(param)
#sys.exit()
head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Referer':'https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
r= requests.post(url,params=param,headers=head)
print(r.text)
data = json.loads(r.text)
get_url='http://116.90.87.38:8094/crack?gt=%s&challenge=%s&success=%s'%(data['gt'],data['challenge'],data['success'])
void = requests.get(get_url)
print(void.text)
#"_ZVING_METHOD=member%2Flogined&_ZVING_URL=%252Fcods%252Fmember%252Flogin&_ZVING_DATA=%7B%7D&_ZVING_DATA_FORMAT=json"
#"_ZVING_METHOD=Gee%2Fverify&_ZVING_URL=%252Fcods%252Fmember%252Flogin&_ZVING_DATA=%7B%22geetest_challenge%22%3A%225f549d347e7a3934c1ab3c99bd643408%22%2C%22geetest_validate%22%3A%2227e6d5cecaf2c1239f9e590bb8392147%22%2C%22geetest_seccode%22%3A%2227e6d5cecaf2c1239f9e590bb8392147%7Cjordan%22%7D&_ZVING_DATA_FORMAT=json"