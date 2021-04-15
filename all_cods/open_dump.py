import json
f = open('dump_nxh_cods.csv','r')
for line in f:
    #print(json.loads(line))
    data = json.loads(line)
    #print(data['统一社会信用代码'])
    data.pop('history')
    for k,v in data.items():
        print(k,v)
#f = open('test_dump.txt','w')
#f.write(json.dumps({'测试':'测试123'}))
