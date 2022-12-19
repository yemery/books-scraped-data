from lxml import html
from bs4 import BeautifulSoup
import requests
import numpy as np
import time
import requests
import csv
from termcolor import colored
import json
import re
from collections import OrderedDict
# Path="C:\Program Files (x86)\chromedriver.exe"
# driver=webdriver.Chrome(Path)
# webPath="https://www.bookdepository.com/bestsellers"
# driver.get(webPath)

# # x btn
# driver.find_element(By.XPATH,'/html/body/div[3]/a[2]/i').click()
# time.sleep(2)
# driver.find_element(By.XPATH,'/html/body/div[1]/a/i').click()
# #next btn
# nextBtn=driver.find_element(By.XPATH,"//*[@id='next-bottom']")


# for i in range(7):
    
#     classBook=driver.find_elements(By.CLASS_NAME,'title')

#     for j in classBook:
#         bookLink=j.find_element(By.TAG_NAME,'a').get_attribute('href')
#         print(bookLink)
#         # with open('urls.txt','a') as f:
#         #     f.write(f'{bookLink}\n')
#     nextBtn.click()
#     time.sleep(2)

# time.sleep(10)
# driver.quit()
def get_Urls():
    for i in range(10):
        url=f"https://www.bookdepository.com/bestsellers?page={i}"
        r=requests.get(url)
        soup=BeautifulSoup(r.content,"html5lib")
        bookName=soup.find_all('h3',{'class':"title"})
        for i in bookName:
            linko=i.find('a')
            link=f"https://www.bookdepository.com{linko['href']}"
            with open('urls.txt','a') as f:
                f.write(f'{link}\n')

get_Urls()