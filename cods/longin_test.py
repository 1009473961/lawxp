import requests
import re
import json
import time
import requests
import sys
import json
import subprocess
import pymongo
db = pymongo.MongoClient(host='127.0.0.1').admin
#db.user_cookie.insert({'mobile':'15350730585','state':'error','password':'10291206nxy','cookie':{}})


head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Referer':'https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}


session = requests.session()
log_url='https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F'

log_r = session.get(log_url,headers=head)
key=re.findall("var key = \'(.*?)\'",log_r.text)[0]
print(session.cookies)
print(key)
password = subprocess.check_output("nodejs psword.js %s %s %s"%(key,key,'10291206nxy'),shell=True)
password = password.decode('utf-8').strip('\\n').strip()
print(password.strip())
#exit()
url='https://www.cods.org.cn/cods/ajax/invoke'
t=int(time.time()*1000)
param={'_ZVING_METHOD':'Gee/tartCaptcha?t=%s'%t,'_ZVING_URL':'%2Fcods%2Fmember%2Flogin','_ZVING_DATA':json.dumps({}),'_ZVING_DATA_FORMAT':'json'}
print(param)
#r= session.post(url,params=param,headers=head)
r= session.post(url,data=param,headers=head)
print(r.text)
data = json.loads(r.text)
print(r.cookies)
#exit()
get_url='http://116.90.87.38:8094/crack?gt=%s&challenge=%s&success=%s'%(data['gt'],data['challenge'],data['success'])
void_response = session.get(get_url)
void_data = json.loads(void_response.text)
print(void_data)

verify_url = 'https://www.cods.org.cn/cods/ajax/invoke'
verify_parse={'_ZVING_METHOD':'Gee/verify',
              '_ZVING_URL':'%2Fcods%2Fmember%2Flogin',
              '_ZVING_DATA':'{"geetest_challenge":"%s","geetest_validate":"%s","geetest_seccode":"%s|jordan"}'%(data['challenge'],void_data['validate'],void_data['validate']),
              '_ZVING_DATA_FORMAT':'json'
              }
print(verify_parse)
verify_response = session.post(verify_url,data=verify_parse,headers=head)

print(verify_response.text)
#exit()
login_params={"_ZVING_METHOD":"member.login",
              "_ZVING_URL":"%2Fcods%2Fmember%2Flogin",
              "_ZVING_DATA":json.dumps({'UserName':'15350730585',
                                        'Password':password,
                                        'geetest_challenge':'xxx,%s,%s'%(data['challenge'],data['challenge']),
                                        'geetest_validate':'xxx,%s,%s'%(void_data['validate'],void_data['validate']),
                                        'geetest_seccode':'xxx,%s|jordan,%s|jordan'%(void_data['validate'],void_data['validate']),
                                        'geetest_challenge_JsonArray':['xxx',data['challenge'],data['challenge']],
                                        'geetest_validate_JsonArray':['xxx',void_data['validate'],void_data['validate']],
                                        'geetest_seccode_JsonArray':['xxx',void_data['validate']+'|jordan',void_data['validate']+'|jordan'],
                                        'Key':key
                                        })
              }
print(login_params)

r = session.post(verify_url,data=login_params,headers=head)
print(r.text)
print('loging_denglu',r.cookies)

get_url= 'https://www.cods.org.cn/cods/ajax/invoke'
url = 'https://ss.cods.org.cn/isearch'
params={'jsonString':'','sign':''}
get_parase={'_ZVING_METHOD':'search/query',
            '_ZVING_URL':'%2F',
            '_ZVING_DATA':'{"type":"1","keywords":"%E9%9D%A2%E5%8C%85"}',
            '_ZVING_DATA_FORMAT':'json'}

get_r = session.post(get_url,headers=head,data=get_parase)
print(get_r.text)
print(get_r.cookies)

get_data=json.loads(get_r.text)

print(get_data['jsonString'])
params['jsonString']=get_data['jsonString']
params['sign'] = get_data['sign']
print(params)
#head.pop('Cookie')
r = session.post(url,data=params,headers=head)

f = open('test_search.html','w')
f.write(r.text)
f.flush()
print(r.cookies)
print(r)
print(session.cookies)

list_info = session.get("https://ss.cods.org.cn/latest/searchR?q=%E9%9D%A2%E5%8C%85&t=common&currentPage=1&scjglx=B",headers=head)

print(list_info.cookies)
print(list_info)
f= open('item_test.html','w')
f.write(list_info.text)
f.flush()

