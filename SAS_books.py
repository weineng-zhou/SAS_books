# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 20:24:11 2020
function: download all PDF books of https://support.sas.com/documentation/cdl_main/94/docindex.html 
@author: weineng.zhou
"""

# 爬虫常用到的模块
import os
import re
import random
import datetime
import time
import requests
import urllib
import pandas as pd
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')

t1 = datetime.datetime.now()
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Safari/537.36'}

currentroot = os.getcwd()

try:
	os.mkdir('SAS_books')
except FileExistsError:
	pass

# 静态方法 不建议 后续得用正则匹配
# url = 'https://support.sas.com/documentation/cdl_main/94/docindex.html'  # 母网页
# response = requests.get(url=url, headers=headers)
# response.encoding = 'utf-8'
# html = response.text


# 动态方法 Xpath方法更方便快捷
url = 'https://support.sas.com/documentation/cdl_main/94/docindex.html'  # 母网页
# driver = webdriver.Chrome(executable_path='chromedriver.exe') # 跳出网页
driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
driver.get(url)
eroot = etree.HTML(driver.page_source)

list_pdf = eroot.xpath('//*[@id="content3"]/div/table/tbody/tr/td[3]/a/@href')
list_name_ = eroot.xpath('//*[@id="content3"]/div/table/tbody/tr/td[1]/text()')
list_name = []
for name in list_name_:
    # 去掉文件名特殊符号
    s = r"[\/\\\:\*\?\？\"\<\>\|\.\+\-\（\）\！\“\”\,\。\{\}\=\%\*\~\·\®\$\&\;\[\]\#\@]"
    title_clean = re.sub(s, '', name).replace('\n','').replace('\t','').replace('\r','')
    list_name.append(title_clean)

# 字典
dic_pdf = dict(zip(list_name,list_pdf))


num=0
for name, pdf_url in dic_pdf.items():
    # print(name, pdf_url)
    try:
        request = urllib.request.Request(pdf_url, headers=headers)
        response = urllib.request.urlopen(request)
        pdf = response.read()
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.reason)
    else:    
        with open('SAS_books/{}.pdf'.format(name), 'wb') as f:
            f.write(pdf)
            num += 1
            time.sleep(random.randint(5,10))
            print('成功下载第{}个PDF: {}.pdf'.format(num, name))
        f.close()


# 耗时计算

# 开始时间
print('开始时间:', t1.strftime('%Y-%m-%d %H:%M:%S'))
# 结束时间
t2 = datetime.datetime.now()
print('结束时间:', t2.strftime('%Y-%m-%d %H:%M:%S'))
delta = t2 - t1

if delta.seconds > 3600:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：'
              + str(int(round(delta.seconds / 3600, 0))) + '时'
              + str(int(round(delta.seconds / 60, 0) % 60)-1) + '分'
              + str(delta.seconds % 60) + '秒')
        
elif delta.seconds > 60:
    if t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] < t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + str(delta.seconds % 60) + '秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] == t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))) + '分'
              + '0秒')
    elif t1.strftime('%Y-%m-%d %H:%M:%S')[-2:] > t2.strftime('%Y-%m-%d %H:%M:%S')[-2:]:
        print('总共耗时：' + str(int(round(delta.seconds / 60, 0))-1) + '分'
              + str(delta.seconds % 60) + '秒')

else:
    print('总共耗时：' + str(delta.seconds) + '秒')

