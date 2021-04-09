from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from pyvirtualdisplay import Display
import sys
import pymongo

import time

#display = Display(visible=0,size=(900,800))
#display.start()
driver=webdriver.Chrome()
driver.get('https://www.cods.org.cn/cods/member/login?SiteID=1&Referer=https%3A%2F%2Fwww.cods.org.cn%2F')
print(driver.title)
#ActionChains(driver).move_to_element(driver.find_element_by_xpath("/html/body/div[3]/div/p/input")).perform()
try:
    down_data_click=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"/html/body/div[3]/div/p/input")))
    time.sleep(1)
    down_data_click.click()
except:
    #未出现确认不需要点击
    pass

userid=driver.find_element_by_xpath('//*[@id="UserName"]')
pswdid=driver.find_element_by_xpath('//*[@id="Password"]')
yanzheng=driver.find_element_by_xpath('//*[@id="captcha"]')
userid.click()
userid.send_keys('15350730585')
time.sleep(1)
pswdid.click()
time.sleep(1)
pswdid.send_keys('123456')
time.sleep(1)
yanzheng.click()
time.sleep(1)
login=driver.find_element_by_xpath('//*[@id="btn"]')
print(driver.get_cookies())







time.sleep(6)
driver.quit()
#display.stop()
