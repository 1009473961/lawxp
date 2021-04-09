#from lxml import etree
#tree = etree.HTML(open('list_page.html','r').read())
#print(tree.xpath("//div[@class='alert alert-info info margin-bottom-none margin-top-xs padding-vertical-none']"))
from fontTools.ttLib import TTFont
font = TTFont('/home/nxh/Desktop/599427.woff2')
cmap=font.getBestCmap()
for k,v in cmap.items():
    print(k,v)
font.saveXML('/home/nxh/Desktop/599427.xml')