import pandas as pd
import requests 
from io import StringIO
import sqlite3

conn = sqlite3.connect('台股.db')
sql = 'Select * from 台股 where 日期="20221201"'

try:
    dfcheck = pd.read_sql(sql, conn)
except:
    dfcheck = pd.DataFrame()
    
if len(dfcheck) == 0:  
    
    url = "https://www.twse.com.tw/zh/exchangeReport/MI_INDEX"
    
    payload ={'response':'csv',
              'date': '20221201',
              'type':'ALLBUT0999'}
    
    resp = requests.post(url, data=payload)
    
    #第一次抓完就註解起來，不然一直執行會被伺服器banned 
    if resp.status_code == 200:
         with open('台股.csv', 'w', encoding='utf-8-sig') as fobj:
             fobj.write(resp.text)
    
    
    #第一步寫入DataFrame進行二維的資料篩選處理
    #twStock = pd.read_csv('台股.csv')
    #但卻出現error，因欄位數預期有7，但卻出現17個的關係
    #因此，先做資料篩選，只選擇下面那些有17欄位的個股資料
    
    #先做開檔動作，用string格式讀取
    with open('台股.csv', 'r', encoding='utf-8-sig') as fobj:
        twstock = fobj.read()
    
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
    df['日期'] = "20221201"
    #df寫入資料庫
    df.to_sql("台股", conn, if_exists="append", index=False)


 

