import requests
import json
import subprocess
import re
head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Referer':'https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
        'Cookie':'JSESSIONID=88A5F09F2B10A8EE62C113398D7C6D2B',
        'Content-Length': '317',
        'Host':'ss.cods.org.cn',
        }

session = requests.Session()
#log_url='https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F'
#log_r = session.get(log_url,headers=head)
#key=re.findall("var key = \'(.*?)\'",log_r.text)[0]
#print(session.cookies)
key= 'd04b5ba2546c4794'
print(key)
password = subprocess.check_output("nodejs psword.js %s %s %s"%(key,key,'10291206nxy'),shell=True)
password = password.decode('utf-8').strip('\\n').strip()
print(password.strip())

url ='https://www.cods.org.cn/cods/ajax/invoke'
challenge='4717edbc61017a63dd0bf113f397175a'
validate='e86e7c435c2f3bddf9b8857a0ec72956'
data='{"geetest_challenge":"%s","geetest_validate":"%s","geetest_seccode":"%s|jordan"}'%(challenge,validate,validate)
verify_parse={'_ZVING_METHOD':'Gee/verify',
              '_ZVING_URL':'%2Fcods%2Fmember%2Flogin',
              #'_ZVING_DATA':{"geetest_challenge":challenge,"geetest_validate":validate,"geetest_seccode":"%s|jordan"%validate},
              '_ZVING_DATA':data,
              '_ZVING_DATA_FORMAT':'json'}
print(verify_parse)
r = requests.post(url,data=verify_parse,headers=head)
print(r.text)
print(r.cookies)

login_params={"_ZVING_METHOD":"member.login",
              "_ZVING_URL":"%2Fcods%2Fmember%2Flogin",
              "_ZVING_DATA":json.dumps({'UserName':'15350730585',
                                        'Password':password,
                                        'geetest_challenge':'xxx,%s,%s'%(challenge,challenge),
                                        'geetest_validate':'xxx,%s,%s'%(validate,validate),
                                        'geetest_seccode':'xxx,%s|jordan,%s|jordan'%(validate,validate),
                                        'geetest_challenge_JsonArray':['xxx',challenge,challenge],
                                        'geetest_validate_JsonArray':['xxx',validate,validate],
                                        'geetest_seccode_JsonArray':['xxx',validate+'|jordan',validate+'|jordan'],
                                        'Key':key
                                        })
              }
print(login_params)

r = session.post(url,data=login_params,headers=head)
print(r.text)
print(r.cookies)

