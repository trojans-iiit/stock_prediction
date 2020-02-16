#import libraries(number crunching)
import pandas as pd
import numpy as np
from datetime import datetime
import pandas_datareader.data as web
from bs4 import BeautifulSoup as bs
import requests
import matplotlib.pyplot as plt

start = datetime(2016,6,8)
end = datetime(2019,6,11)
stocklist = ['AAPL','GOOG','FB','AMZN','COP','INFY','IBM','QCOM','ADBE','WMT',]#APPLE,GOOGLE,FACEBOOK,AMAZON etc
p = web.DataReader(stocklist, 'yahoo',start,end)
p
data=pd.DataFrame(p)
#getting data
data

simple_returns1 = (data / data.shift(1)) - 1
len(simple_returns1)
simple_returns1.head(20)
log_returns = np.log(data / data.shift(1))
log_returns.head()
data["Close"].plot(label="DAL",figsize=(16,8),title="adjusting closing price")
#simple_returns1["Close"][comp_name]
wt=[]
for i in range(0,757):
  wt.append(i)
wt
def calc_best_stock(a,b,comp_name1,comp_name2):
  temp=0
  for i in range(1,756):
    temp+=(a[i]-b[i])*wt[i]
  if temp>=0:
    print(temp)
    return comp_name1
  else:
    print(temp)
    return comp_name2

budget=int(input("enter your budget"))
comp_name1=input("enter comany code")
comp_name2=input("enter the second company name")
result=calc_best_stock(simple_returns1["Close"][comp_name1],simple_returns1["Close"][comp_name2],comp_name1,comp_name2)
result