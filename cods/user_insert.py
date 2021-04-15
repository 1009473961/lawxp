import pymongo
import random
db = pymongo.MongoClient('127.0.0.1').admin

pw = 'Abcd@123'
for user in ['18910628269','13301242741']:
    #db.user_cookie.insert({'mobile':user,'password':pw,'state':'login_again','type':'enterprise'})

    db.user_cookie.update({'mobile': user}, {'$set': {'jsessionid': '', 'state': 'login_again'}})
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