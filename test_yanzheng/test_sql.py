# -*- coding: utf-8 -*-
import pymssql
import datetime
import json
import re
keys = [
    #'id',
    '注册资本',
    '经营状态',
    'old_title',
    '经济行业',
    '经营期限',
    '登记号',
    '法定代表人或负责人姓名',
    '经营范围',
    '统一社会信用代码',
    'title',
    '成立日期',
    '经济类型',
    '最后更新日期',
    '注册地址',
    '机构类型',
    '批准机构名称',
    #'histoy'
]

print(keys)
#exit()
sql = pymssql.connect(host='127.0.0.1',user='sa',password='Nn10291206',database='test_nxh',tds_version='7.0')

#if sql:
#    print("连接成功!")
#    print(sql)
cursor = sql.cursor()
#cursor.execute("insert into data_info values('001')")   #执行sql语句
#添加字段

for key in keys:
    print(key)

sql_creata = "create table data_info(注册资本 nvarchar(200)," \
             "经营状态 nvarchar(200)," \
             "历史标题 nvarchar(200)," \
             "经济行业 nvarchar(200)," \
             "经营期限 nvarchar(200)," \
             "登记号 nvarchar(200),""" \
             "法定代表人或负责人姓名 nvarchar(200)," \
             "经营范围 nvarchar(max)," \
             "统一社会信用代码 nvarchar(50)," \
             "标题 nvarchar(max)," \
             "成立日期 nvarchar(50)," \
             "经济类型 nvarchar(200)," \
             "最后更新日期 nvarchar(50)," \
             "注册地址 nvarchar(max)," \
             "机构类型 nvarchar(200)," \
             "批准机构名称 nvarchar(200))"
#print(sql_creata)
#cursor.execute(sql_creata)
#sql.commit()
#exit()
#cursor.execute("create table data_info(注册资本 nvarchar(200),经营状态 nvarchar(200),历史标题 nvarchar(200),经济行业 nvarchar(200),经营期限 nvarchar(200),登记号 nvarchar(200),"
#               "法定代表人或负责人姓名 nvarchar(200),经营范围 nvarchar(max))")

# for key in keys:
#     print(key)
#     linsql = "alter table data_info add %s nvarchar()"%key
#     print(linsql)
#     cursor.execute("alter table data_info add %s nvarchar"%key)


data = {
          '最后更新日期': '未公示',
          'old_title': 'sd',
          'title': '资溪县面包产业发展办公室',
          '成立日期': '未公示',
          '批准机构名称': '资溪县编委会',
          '机构类型': '事业单位',
          '法定代表人或负责人姓名': '曾长华',
          '注册地址': '资溪县建设中路号',
          '注册资本': '18',
          '登记号': '未公示',
          '经济类型': '未公示',
          '经济行业': '未公示',
          '经营期限': '2018-01-082023-01-08',
          '经营状态': '正常',
          '经营范围': '服务产业,服务面包户为面包生产,经营者提供信息劳务,法律服务',
          '统一社会信用代码': '12361129799463929',
           }
info=[]
for k in keys:
    print(k,data[k])

    print(type(data[k]))
    info.append(data[k])

print(len(info))
insql = "insert into data_info values(N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s',N'%s')"%tuple(info)
print(insql)

cursor.execute(insql)

sql.commit()  # 提交执行

#r = cursor.fetchall()
#print(r)






#sql.close()  # 关闭游标
#sql.close()  # 关闭连接