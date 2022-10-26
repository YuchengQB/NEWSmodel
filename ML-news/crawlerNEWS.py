'''自由時報、中國時報、TVBS 新聞抓取'''

'''
    一、自由時報LTN
    新聞的網頁原始碼結構，
    可以發現整個新聞區塊都是在<div class="whitecon boxTitle..."> 之下
    而每篇新聞都是在其下的每個<li>標籤內
    其中，新聞標題都是在標籤<a class="tit"> 中 <div> 之下 <h3>標籤 的值
    必須下拉換頁
    
    二、中國時報CHDTV
    中國時報標題xpath不適用
    使用find_element_by_class_name定位
    可利用網址換頁
    
    三、TVBS
    雖然新聞標題都是在<li>中，但每隔四則就會有一個空白<li>要跳過
    下拉式
    
'''

from selenium import webdriver
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  #可以用time.localtime(time.time())擷取時間
'''擷取此網頁的原始資料，得到一個回應物件res'''
#res=requests.get(URL)
'''將網頁資料進行解析'''
#bs = BeautifulSoup(res.text,'lxml')

"""自由時報"""

'''Driver 進網頁'''
driver = webdriver.Chrome("D:\chromedriver\chromedriver")
driver.implicitly_wait(1)
URL = "https://news.ltn.com.tw/list/breakingnews"
driver.get(URL)

'''下拉到網頁底部以載入所有資料'''
for i in range(1,20):    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)

'''爬網頁資料'''
LTNnewstitle=[]
for newsnumber in range(1,210): #抓個2頁多
    
    newsnumber=str(newsnumber)
    titlepath="/html/body/div[9]/section/div[3]/ul/li["+newsnumber+"]/a[2]/div/h3"
    a=driver.find_element_by_xpath(titlepath)

    print(a.text)
    LTNnewstitle.append(a.text)

LTN_all={"NEWS":LTNnewstitle,"Writer":"LTN"}
LTN_df=pd.DataFrame(LTN_all)    


"""中國時報"""
CHDTVnewstitle=[]
for choosepage in range(1,10): #抓1到5頁 一頁24則
    
    URL = "https://www.chinatimes.com/realtimenews/?page="+str(choosepage)+"&chdtv"
    driver.get(URL)
    
    
    a = driver.find_elements_by_class_name("title")
    for eachtitle in a:
        newstitle = eachtitle.text

        print(newstitle)
        CHDTVnewstitle.append(newstitle)
        

CHDTV_all={"NEWS":CHDTVnewstitle,"Writer":"CHDTV"}
CHDTV_df=pd.DataFrame(CHDTV_all)


"""TVBS"""
driver.implicitly_wait(1)
URL = "https://news.tvbs.com.tw/realtime"
driver.get(URL)


'''下拉到網頁底部以載入所有資料'''
for i in range(1,10):    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)


TVBSnewstitle=[]
for newsnumber in range(1,210): #抓個2頁多
    newsnumber=str(newsnumber)
    titlepath="/html/body/div[1]/main/div/article/div[2]/div[3]/ul/li["+newsnumber+"]/a[1]/h2"
    try:
        a=driver.find_element_by_xpath(titlepath)
    except:
        continue


    print(a.text)
    TVBSnewstitle.append(a.text)

TVBS_all={"NEWS":TVBSnewstitle,"Writer":"TVBS"}
TVBS_df=pd.DataFrame(TVBS_all)


"""UDN聯合新聞"""
driver.implicitly_wait(1)
URL = "https://udn.com/news/breaknews/1"
driver.get(URL)
'''下拉到網頁底部以載入所有資料'''
for i in range(1,20):    
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(3)
'''爬網頁資料'''
UDNnewstitle=[]
for newsnumber in range(1,210): #抓個2頁多
    
    newsnumber=str(newsnumber)
    titlepath="/html/body/main/div/section[2]/section/div[1]/section/div["+newsnumber+"]/div[2]/h2/a"
    a=driver.find_element_by_xpath(titlepath)

    print(a.text)
    UDNnewstitle.append(a.text)

UDN_all={"NEWS":UDNnewstitle,"Writer":"UDN"}
UDN_df=pd.DataFrame(UDN_all) 


"""關閉Chromedriver"""
driver.close()


""" DataFrame合併、index順排下去 """
NEWSdataframe=pd.concat([LTN_df,CHDTV_df,TVBS_df,UDN_df],ignore_index=True)


'''建立CSV檔案，把dataframe寫進csv檔中'''
import csv
import time  #可以用time.localtime(time.time())擷取時間


fname= time.strftime("%m%d_%H_%M", time.localtime())+"_新聞.csv"
NEWSdataframe.to_csv(fname,index=False,encoding="utf_8_sig",sep=',')

















