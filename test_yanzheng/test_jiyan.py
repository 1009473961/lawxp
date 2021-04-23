import requests
import re
import json
import time
import requests
import sys
import json
import subprocess
import pymongo
import random
session = requests.session()

head={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Referer':'https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}
url = 'https://www.cods.org.cn/cods/ajax/invoke'



for i in range(100):
        t = int(time.time() * 1000)
        param = {'_ZVING_METHOD': 'Gee/tartCaptcha?t=%s' % t, '_ZVING_URL': '%2Fcods%2Fmember%2Flogin',
                     '_ZVING_DATA': json.dumps({}), '_ZVING_DATA_FORMAT': 'json'}
        #print(param)
        r = session.post(url, data=param, headers=head)
        print(r.text)
        data = json.loads(r.text)
        #print(r.cookies)
        get_url = 'http://116.90.87.38:8094/crack?gt=%s&challenge=%s&success=%s' % (data['gt'], data['challenge'], data['success'])

        void_response = session.get(get_url)
        void_data = json.loads(void_response.text)
        print(void_data)
