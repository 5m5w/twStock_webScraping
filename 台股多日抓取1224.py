import requests
import pandas as pd
from io import StringIO
import sqlite3
import time

conn = sqlite3.connect('台股作業1225.db')

dateRange = pd.date_range('20220101', '20220105')

for i in dateRange:
    dRange = str(i)[:10].replace('-','')
    print(dRange)
    
    sql = 'Select * from ‘台股作業1225’ where 日期＝"' + dRange + '"'
    
    try:
        dfcheck = pd.read_sql(sql, conn)
    except:
        dfcheck = pd.DataFrame()
    
    if len(dfcheck) == 0:
        time.sleep(5)
        
        url = "https://www.twse.com.tw/zh/exchangeReport/MI_INDEX"
        payload = {'response':'csv',
                   'date': dRange ,
                   'type':'ALLBUT0999'}
        
        resp = requests.post(url, data=payload)
        # resp.encoding="utf-8-sig"
        # if resp.status_code == 200:
        #     with open('所有股票-作業.csv', 'w') as fobj:
        #         fobj.write(resp.text)
                
        totalStocks=''
        if resp.status_code == 200 and len(resp.text) != 0:
            stocks = resp.text
            split_data = stocks.split('\n')
        
            for i in split_data:
                if len(i.split('",')) == 17:            
                    totalStocks += i +'\n'
                    
            df = pd.read_csv(StringIO(totalStocks))
            df = df.iloc[:,:-1]
            df.iloc[:,0] = df.iloc[:,0].str.replace('="','').str.replace('"','')
            
            for i in range(2,16):
                if (i != 9) and df.iloc[:,i].dtype=='object':
                    df.iloc[:,i] = df.iloc[:,i].str.replace(',','')
                    df.iloc[:,i] = pd.to_numeric(df.iloc[:,i], errors="coerce")
                    
            df['日期'] = dRange
            df.to_sql('台股作業1225', conn, if_exists='append', index=False)