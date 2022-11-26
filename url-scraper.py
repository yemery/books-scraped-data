from selenium import webdriver
from selenium.webdriver.common.by import By
import time

Path="C:\Program Files (x86)\chromedriver.exe"
driver=webdriver.Chrome(Path)
webPath="https://www.bookdepository.com/bestsellers"
driver.get(webPath)

# x btn
driver.find_element(By.XPATH,'/html/body/div[3]/a[2]/i').click()
time.sleep(2)
driver.find_element(By.XPATH,'/html/body/div[1]/a/i').click()
#next btn
driver.find_element(By.XPATH,"//*[@id='next-bottom']")
for i in range(7):
    #book classes
    classBook=driver.find_elements(By.CLASS_NAME,'title')
    for j in classBook:
        bookLink=j.find_element(By.TAG_NAME,'a').get_attribute('href')
        with open('urls.txt','a') as f:
            f.write(f'{bookLink}\n')
    time.sleep(2)

time.sleep(10)
driver.quit()
