import csv
import yfinance as yf
import pandas as pd
stockticker = input("Enter stock ticker name:")
fi = yf.Ticker(stockticker)
marketdata= fi.history(start = "1996-1-01", end = "2022-6-30")
print(marketdata)
Open = marketdata["Open"]
Close = marketdata["Close"]
print(Open)
print(Close)
print(len(Close))
array = []
lenstuff = len(Close)
for i in range(lenstuff):
    sum = 0
    for x in range(10):
    
        sum = sum + Close[i - x]
    tendaymovingaverage = sum/10
    
    array.append(tendaymovingaverage)
print(array)
twentyarray = []
for i in range(lenstuff):
    sum = 0
    for x in range(20):
    
        sum = sum + Close[i - x]
    twentydaymovingaverage = sum/20
    twentyarray.append(twentydaymovingaverage)
#print(twentyarray)
fiftyarray = []
for i in range(lenstuff):
    sum = 0
    for x in range(50):
    
        sum = sum + Close[i - x]
    fiftydaymovingaverage = sum/50
    fiftyarray.append(fiftydaymovingaverage)
#print(fiftyarray)
marketdata["fifty"]=fiftyarray
marketdata["twenty"]=twentyarray
df = marketdata[["Open","Close","fifty","twenty"]]
print(marketdata)

df.to_csv("Users\justin\Documents\GitHub\Stock-algorithm\Stock Data" + f"{stockticker}.csv")