import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect('台股作業.db')
sql = 'Select * from 台股作業'
df = pd.read_sql(sql,conn)
# df = pd.read_sql('Select * from 台股作業', conn, index_col="證券代號")

# 一年的平均股價
# stocks_year_mean_price = df.groupby('證券名稱')['開盤價'].mean().sort_values(ascending=False)

# 產業類股票 
tourismStocks1 = ('2614','2719','2731','2734','2743','2745','5706')
tour = pd.DataFrame(tourismStocks1)


# =============================================================================
# # 讀取每支股票在特定時間的股價，存成陣列
# da=[]
# for i in df.iloc[0:10,0]:
#     for x in df.iloc[0:10, 7]:
#         da += [[i,x]]
# # 存入dataframe      
# df1 = pd.DataFrame(da)
# 
# # 抓取股票名稱
# s=[]
# for y in df1[:][0]:
#     s += [y]
# 
# # 把股票名稱當成index，以便用loc抓取
# df1.index=[s]
# u = df1.loc[s].mean()
# 
# =============================================================================
