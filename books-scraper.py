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


def get_books_links():
    links=[]
    with open('urls.txt','r') as f:
        flines=f.readlines()
        for i in flines:
            if i.strip()=="":
                continue
            links.append(i.strip("\n"))
    return links
# print(get_books_links())
def get_book_data():
    books=[]
    booksLinks=get_books_links()
    for i in range(0,len(booksLinks)):
        URL=booksLinks[i]
        r=requests.get(URL)
        soup=BeautifulSoup(r.content,'html5lib')

        containerImg=soup.find('div',{'class':"item-img-content"})
        image=containerImg.find('img').attrs['src']
        # print(image)

        containerDiv=soup.find('div',{'class':"item-info"})
        title=containerDiv.find('h1').text
        # print(f'"{title}"')
        
        desc=soup.find("div",{'class':"item-excerpt trunc"})
        repdesc=desc.text.replace("show more","")
        regexDesc=re.sub("\s{2,}"," ",repdesc)
        # print(regexDesc)
        # print(f'"{repdesc.strip()}"')
        # description=desc
        NameContainer=containerDiv.find('div',{'class':'author-info hidden-md'})
        authorName=NameContainer.find_all('span')[1].text.strip()
        # print(authorName)

        price=soup.find('span',{'class':'sale-price'}).text[3:]
        # print(price)

        bookDetails=soup.find('ul',{'class':'biblio-info'}).find_all('li')
        detailsIndex=[0,2,4,5]
        # print(bookDetails)
        dList=[]
        for k in range(len(bookDetails)):
            if k in detailsIndex:
                spanLi=bookDetails[k].find('span').text
                # print(re.sub("\s{1,}"," ",f'"{spanLi.strip()}"'))
                strfinal=re.sub("\s{1,}"," ",spanLi)
                dList.append(strfinal.strip())
        # print(dList)
        format,publication_date,publication_city_country,language=[q for q in dList]
        # print(format,publication_date,publication_city_country,language)
        keys=['id','image','title','description','author_name','price,',"format","publication_date","publication_city_country","language"]
        values=[i,image,title,regexDesc,authorName,price,format,publication_date,publication_city_country,language]
        book={}
        for e in range(len(keys)):
            book[keys[e]]=values[e]
        books.append(book)
        # print(book)

    return books

        
# print(get_book_data())   
def Json_file():
    books=get_book_data()
    with open('books_data.json','w',encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(books,indent=4))

if __name__ == "__main__":
    start_time = time.time()
    print(colored("Start...\n",'blue'))
    Json_file()
    print(colored("\nDone :)","blue"))
    print(colored("--- %s seconds ---"%(time.time() - start_time),"yellow"))





