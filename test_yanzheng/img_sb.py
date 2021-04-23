from PIL import Image
import pytesseract
import time
import re




c = open('image_load.csv','w')
def convert_img(img,threshold):
    """灰度加二极化"""
    img = img.convert("L")  # 处理灰度
    pixels = img.load()
    print(pixels[-1,-1])
    for x in range(img.width):
        for y in range(img.height):
            if pixels[x, y] > threshold:
                pixels[x, y] = 255
            else:
                pixels[x, y] = 0
    #print(pixels[-1,-1])
    return img




def depoint(img,i):
    """传入二值化后的图片进行降噪"""
    pixdata = img.load()
    w,h = img.size
    max_num = 90
    for y in range(1,h-1):
        for x in range(1,w-1):
            count = 0
            if pixdata[x,y-1] > max_num:#上
                count = count + 1
            if pixdata[x,y+1] > max_num:#下
                count = count + 1
            if pixdata[x-1,y] > max_num:#左
                count = count + 1
            if pixdata[x+1,y] > max_num:#右
                count = count + 0.5
            if pixdata[x-1,y-1] > max_num:#左上
                count = count + 0.5
            if pixdata[x-1,y+1] > max_num:#左下
                count = count + 0.5
            if pixdata[x+1,y-1] > max_num:#右上
                count = count + 0.5
            if pixdata[x+1,y+1] > max_num:#右下
                count = count + 0.5
            if count >= 4 :
                pixdata[x,y] = 255
    return img

file = '/home/nxh/Desktop/4051.png_860.png'




img = Image.open(file)

#for i in range(1,200,10):
for i in range(1):
    #print(i)
    #file = '/home/nxh/Desktop/test_lianzhong/test_range_%s.png'%5
    file = '/home/nxh/Desktop/test_lianzhong/test_png_py.jpng'
    #file = '/home/nxh/Desktop/test_lianzhong/test_muggle.png'
    img = Image.open(file)
    img = convert_img(img ,90)
    #exit()
    #img.show()
    #exit()
    #time.sleep(5)
    img_jz = depoint(img,i)
    #img_jz.save('one.png')
    #img_rh = convert_img(img_jz,100)
    img_jz.show()
    #img_jz.save('test_muggle.png')

    w = pytesseract.image_to_string(img_jz)
    info = re.findall('\w+',w)
    print(repr(info))
    time.sleep(5)
#image = Image.open(file)
#image.show()


'123456abcderg'

