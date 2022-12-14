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



def get_books_links():
    links=[]
    with open('urls.txt','r') as f:
        flines=f.readlines()
        for i in flines:
            if i.strip()=="":
                continue
            links.append(i.strip("\n"))
    return links
categories=[]
def get_book_data():
    books=[]
    booksLinks=get_books_links()
    for i in range(0,len(booksLinks)):
        print(i)
        URL=booksLinks[i]
        r=requests.get(URL)
        soup=BeautifulSoup(r.content,'html5lib')

        containerImg=soup.find('div',{'class':"item-img-content"})
        image=containerImg.find('img').attrs['src']
        # print(image)

        containerDiv=soup.find('div',{'class':"item-info"})
        title=containerDiv.find('h1').text
        regexTitle=re.sub("\s{2,}|,"," ",title)
        # print(f'"{title}"')
        
        desc=soup.find("div",{'class':"item-excerpt trunc"})
        repdesc=desc.text.replace("show more","")
        regexDesc=re.sub("\s{2,}|,"," ",repdesc)
        # print( regexDesc)
      
        # print(f'"{repdesc.strip()}"')
        # description=desc
        NameContainer=containerDiv.find('div',{'class':'author-info hidden-md'})
        authorName=NameContainer.find('span').find('span').text.strip()
        # regexAuthor=re.sub("\s{2,}|,"," ",authorName)
        print(authorName)

        price=soup.find('span',{'class':'sale-price'}).text
        # print(price)

        bookDetails=soup.find('ul',{'class':'biblio-info'}).find_all('li')
        detailsIndex=[0,2,4,5]
        # print(bookDetails)
        cat=soup.find('ol',{'class':'breadcrumb'}).find_all('li')
        catList=[]
        for z in cat[1:]:
            catName=re.sub("\s{2,}"," ",z.text).strip()
            catNameWithoutSpChar=re.sub('[^A-Za-z]+', ' ', catName)
            categories.append(catNameWithoutSpChar)
            catList.append(catNameWithoutSpChar)

        # print(catList)
        catList=list(dict.fromkeys(catList))
        # print(len(categories))



        dList=[]
        for k in range(len(bookDetails)):
            if k in detailsIndex:
                spanLi=bookDetails[k].find('span').text
                # print(re.sub("\s{1,}"," ",f'"{spanLi.strip()}"'))
                strfinal=re.sub("\s{1,}|,"," ",spanLi)
                dList.append(strfinal.strip())
        # print(dList)
        format,publication_date,publication_city_country,language=[q for q in dList]
        # print(format,publication_date,publication_city_country,language)
        keys=['id','image','title','description','author_name','price',"format","publication_date","publication_city_country","language",'tags']
        values=[i,image,regexTitle,regexDesc,authorName,price,format,publication_date,publication_city_country,language,';'.join(catList)]
        book={}
        for e in range(len(keys)):
            book[keys[e]]=values[e]
        books.append(book)


    return books

def csv_cat():
    catList=[]
    books=get_book_data()
    newCarList=list(set(categories))
    removedups=list(dict.fromkeys(newCarList))
    for i in range(len(removedups)):
        catDict={}
        catDict['id']=i
        catDict['category_name']=removedups[i]
        catList.append(catDict)
    with open("books_cats.csv", 'w',encoding="utf-8") as csvfile: 
        writer = csv.DictWriter(csvfile, fieldnames =['id','category_name']) 
        writer.writeheader() 
        # writing data rows 
        writer.writerows(catList) 
        print(colored("added secc...\n",'blue'))

def csv_file():
 
    '''
'''

    input = open("books_data.json")
    data = json.load(input)
    input.close()
    output = csv.writer(open("books_data.csv",'w'))
    output.writerow(data[0].keys())  # header row
    for row in data:
        output.writerow(row.values())

 


  
def Json_file():
    books=get_book_data()
    with open('books_data.json','w',encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(books,indent=4))

if __name__ == "__main__":
    start_time = time.time()
    print(colored("Start...\n",'blue'))
    # Json_file()
    csv_file()
    # csv_cat()
    # get_book_data()


    # book=get_book_data()
    print(colored("\nDone :)","blue"))
    print(colored("--- %s seconds ---"%(time.time() - start_time),"yellow"))





