import redis

redis_db = redis.Redis(host='127.0.0.1',port=6379)

#word='面包'
f = open('/home/share/start_all_info.csv','r')


for line in f:
    #word = url.find
    word = line.strip().split(',')[2]
    word_url = 'https://ss.cods.org.cn/latest/searchR?q=%s&t=common&currentPage=1&scjglx=B'%word

    redis_db.lpush('redis_code_word:start_urls',word_url)
    print(word_url)

