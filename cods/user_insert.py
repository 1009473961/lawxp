import pymongo
import random
db = pymongo.MongoClient('127.0.0.1').admin

pw = 'Abcd@123'
for user in ['17310273245',#8001 5
          '17310464023',#8001，7
          '17310264793',#8001,10
          '17718521532',#8000,2
          '17710464571',
          '15311916734',
          '17310295613',
          '17710477046',
          '15313844063',
          '17718592135',
          '17310262147',
          '15301162524',
          '17777843601',
          '17777840537',
          '17710279326'
          ]:
    db.user_cookie.insert({'mobile':user,'password':pw,'state':'login_again','type':'enterprise','jsessionid':''})

    #db.test_cookie.update({'mobile': user}, {'$set': {'jsessionid': '', 'state': 'login_again'}})
#username='17310374212'
#value='70BFEADFC9C5A42E35D1C3A0388E6EEB'

#db.user_cookie.update({'mobile':username},{'$set':{'jsessionid':value,'state':'available'}})
exit()
def get_cook():
    jsessionid_list = [x['jsessionid'] for x in db.user_cookie.find({'state':'available'})]
    cook = {'JSESSIONID': random.choice(jsessionid_list)}
    print(jsessionid_list)
    return cook

for i in range(5):
    #print(get_cook())
    cook = get_cook()
    if cook['JSESSIONID'] == '70BFEADFC9C5A42E35D1C3A0388E6EEB':
        print('update')
        db.user_cookie.update_one({'jsessionid':cook['JSESSIONID']},{'$set':{'state':'noavailable'}})
    print(cook)