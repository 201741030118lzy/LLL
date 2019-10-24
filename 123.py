import requests
from bs4 import BeautifulSoup
import multiprocessing as mp
import time

t1=time.time()
r=requests.get('https://movie.douban.com/')

c=r.text

soup=BeautifulSoup(c,'html.parser')
#content=soup.find_all('div',{'class':'list-cont'})
page_div=soup.find('div',{'class':'page'})
#page=page_div.find_all('a')[-2].text
cars=[]

urls=['https://movie.douban.com/'+str(i)+'.html' for i in range(1,3)]

def crawl_page(url):
    p_r=requests.get(url)
    p_c=p_r.text
    p_soup=BeautifulSoup(p_c,'html.parser')
    p_content=p_soup.find_all('div',{'class':'list-cont'})
    pageSto=[]
    for car in p_content:
        stoDic={}
        stoDic['picUrl']=car.find('div',{'class':'list-cont-img'}).find('img')['src']
        stoDic['name']=car.find('div',{'class':'list-cont-main'}).find('a').text
        try:
            stoDic['score']=car.find('span',{'class':'score-number'}).text
        except Exception as e:
            stoDic['score']=''

        pageSto.append(stoDic)
    return pageSto

pool=mp.Pool()
multi_res=[pool.apply_async(crawl_page,(url,))for url in urls]
pageCars=[res.get() for res in multi_res]

print(len(cars))
t2=time.time()
print(t2-t1)

