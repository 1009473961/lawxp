import requests
import json
import datetime
session=requests.session()
url = 'https://ss.cods.org.cn/isearch'
get_url= 'https://www.cods.org.cn/cods/ajax/invoke'

params={'jsonString':'%257B%2522type%2522%253A%25221%2522%252C%2522keywords%2522%253A%2522%2525E9%25259D%2525A2%2525E5%25258C%252585%2522%252C%2522usermobile%2522%253A%2522%2522%252C%2522token%2522%253A%2522%2522%257D','sign':'86a2522dc4b7d4eed5691faec44b6a28'}
#params['jsonString'] = '%7B%22type%22%3A%221%22%2C%22keywords%22%3A%22%25E9%259D%25A2%25E5%258C%2585%22%2C%22usermobile%22%3A%222843ca8220f5ecf815e2f5c39a9757f4%22%2C%22token%22%3A%22e52b8974e28d758050b2b9121f6a107f%22%7D'
#params['sign'] = '93bf4252782c281707b4606361f959a5'
head = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.9',
        'Connection':'keep-alive',
        'Referer':'https://www.cods.org.cn/',
        'Origin':'https://www.cods.org.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'}

head['Cookie']='JSESSIONID=1D3E87B46ED8BA9865A10251BC47F939'
get_parase={'_ZVING_METHOD':'search/query',
            '_ZVING_URL':'%2F',
            '_ZVING_DATA':'{"type":"1","keywords":"%E9%9D%A2%E5%8C%85"}',
            '_ZVING_DATA_FORMAT':'json'}
'''
get_r = session.post(get_url,headers=head,data=get_parase)
print(get_r.text)
get_data=json.loads(get_r.text)
#exit()
print(get_data['jsonString'])
params['jsonString']=get_data['jsonString']
params['sign'] = get_data['sign']
print(params)
head.pop('Cookie')
r = session.post(url,data=params,headers=head)
f = open('test_search.html','w')
f.write(r.text)
f.flush()
print(r.cookies)
print(r)
print(session.cookies)
'''
head['Cookie']='JSESSIONID=DD9DD89E80ECC7076FB16ACD929B359E'
s = session.cookies
s.set('JSESSIONID','DD9DD89E80ECC7076FB16ACD929B359E',path='/', domain='ss.cods.org.cn')
print(session.cookies)

#exit()
list_info = session.get("https://ss.cods.org.cn/latest/searchR?q=%E9%9D%A2%E5%8C%85&t=common&currentPage=1&scjglx=B",headers=head)

print(list_info.cookies)
print(list_info)
f= open('item_test.html','w')
f.write(list_info.text)
f.flush()