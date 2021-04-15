# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from all_cods.items import AllCodsItem,AllCodsList
import datetime
class AllCodsPipeline:
    def __init__(self):
        self.fb=None
    def open_spider(self,spider):
        t = datetime.datetime.now()
        t_time = t.strftime('%Y_%-m_%-d')

        self.fb = open('dump_nxh_cods_%s.csv'%t_time,'a+')
        self.fb_list = open('dump_nxh_list_word_%s.csv'%t_time,'a+')


    def process_item(self, item, spider):
        if isinstance(item,AllCodsItem):
            data = item['data']
            history = item['history']
            data['history'] = history
            self.fb.write(json.dumps(data)+'\n')
            self.fb.flush()
            return item
        if isinstance(item,AllCodsList):
            self.fb_list.write('%s,%s，%s\n'%(item['word'],item['url'],item['type_word']))
            self.fb_list.flush()
            return item
    def close_spider(self,spider):
        self.fb.close()

