# 程式碼來自「單日台股資料抓取」的延伸

import pandas as pd
import requests 
from io import StringIO
import sqlite3
import time

conn = sqlite3.connect('台股.db')

#抓取時間範圍
dayRange = pd.date_range('20220101','20221219')

#注意! type(dRange)是特殊的時間戳記型態，不能直接做字串的處理，#所以先轉成字串格式，並取需要的年月日的值，且將"-"移除
for dRange in dayRange:
    correct_dayRange = str(dRange)[:10].replace('-', '')
#將下面的有時間的程式碼換成都 correct_dayRange
    
    sql = 'Select * from 台股 where 日期="' + correct_dayRange + '"'
    
    try:
        dfcheck = pd.read_sql(sql, conn)
    except:
        dfcheck = pd.DataFrame()
        
    if len(dfcheck) == 0:  
        time.sleep(5)
        url = "https://www.twse.com.tw/zh/exchangeReport/MI_INDEX"
        
        payload ={'response':'csv',
                  'date': correct_dayRange,
                  'type':'ALLBUT0999'}
        
        resp = requests.post(url, data=payload)
        
    ### ==============檔案直接寫入sqlite，所以這中間就不需要了=========    
        # if resp.status_code == 200:
        #      with open('台股.csv', 'w', encoding='utf-8-sig') as fobj:
        #          fobj.write(resp.text)
        # #第一步寫入DataFrame進行二維的資料篩選處理
        # #twStock = pd.read_csv('台股.csv')
        # #但卻出現error，因欄位數預期有7，但卻出現17個的關係
        # #因此，先做資料篩選，只選擇下面那些有17欄位的個股資料
        # #先做開檔動作，用string格式讀取
        # with open('台股.csv', 'r', encoding='utf-8-sig') as fobj:
        #     twstock = fobj.read()
    ### ==============刪除=============
        #如果是國定假日，證券交易所網站是不會有資料的，所以在這裡建200驗證，以及當沒有資料時，就不進行以下的檔案抓取
        if resp.status_code==200 and len(resp.text)!=0:
            #在這裡將resp取到的網頁資料存入twstock
            twstock = resp.text
        
            #透過分行\n將每一筆個股做分割成單一行的資料    
            split_list = twstock.split('\n')
            #放進迴圈，再將個股內部的各個資料做欄位的分割
            stocks =''
            for i in split_list:
                #每個個股的17筆資料，是我們要的
                #print(len(i.split('",')))
                #因此，透過if判斷，篩選出這些17筆資料，存入stocks空字串
                if len(i.split('",')) == 17:
                    stocks += i +'\n'
                    
            #成功得到stocks的完整資料後，就可以放入dataframe了
            #df = pd.read_csv(stocks)
            #可是在variable explorer找不到df的資料
            #那是因為read_csv讀的是檔案或網址，但stocks是大字串
            #所以要將stocks字串，轉成pandas，來騙dataframe
            #最上方加入套件 from io import StringIO
            df = pd.read_csv(StringIO(stocks))
            
            #點開df可以發現最後一欄是我們不需要的資料
            df = df.iloc[:, :-1]
            
            #將df裡面的數字字串都轉為數值格式（紅色底)
            #並把數值內的','刪除，形成單純的數值型態
            for i in range(2,16):
                if (i != 9) and df.iloc[:, i].dtype == 'object':
                    df.iloc[:, i] = df.iloc[:, i].str.replace(',','')
                    df.iloc[:, i] = pd.to_numeric( df.iloc[:, i], errors='coerce')
            #將第0欄的證券代號不必要的符號刪除
            df.iloc[:,0] = df.iloc[:,0].str.replace('="','').str.replace('"','')
            
            #加入日期，寫入sqlite
            df['日期'] = correct_dayRange
            #df寫入資料庫
            df.to_sql("台股", conn, if_exists="append", index=False)
    
    
     
    
