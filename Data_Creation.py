import csv
import yfinance as yf
import pandas as pd
import os
def getStockData(stockTicker, endDate = "2022-7-25"):
    stockticker = stockTicker
    fi = yf.Ticker(stockticker)
    marketdata= fi.history(start = "1995-1-01", end = endDate)
    #print(marketdata)
    Open = marketdata["Open"]
    Close = marketdata["Close"]
    #print(Open)
    #print(Close)
    #print(len(Close))
    array = []
    lenstuff = len(Close)
    for i in range(lenstuff):
        sum = 0
        for x in range(200):
            
           sum = sum + Close[i - x]
        tendaymovingaverage = sum/200

        array.append(tendaymovingaverage)
    #print(array)
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
    marketdata["Fifty DMA"]=fiftyarray
    marketdata["Twenty DMA"]=twentyarray
    marketdata["Two Hundred DMA"] = array
    df = marketdata[["Open","Close","Fifty DMA","Twenty DMA", "Two Hundred DMA"]]
#print(marketdata)
    directory = "Stock-Data"
    parentDir = "Documents\GitHub\Stock-algorithm"
    path = os.path.join(parentDir, directory)
    df.to_csv(path + "\\" + stockticker + ".csv")
