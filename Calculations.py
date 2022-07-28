from asyncore import read
from curses import start_color
import pandas as pd
import Data_Creation 
import csv
import os
from datetime import date

directory = "Stock-Data"
parentDir = "Documents\GitHub\Stock-algorithm"
path = os.path.join(parentDir, directory)
today = date.today()

#function that returns a csv file of the data asked for
def startCalc(tickerName, startDate = "1996-01-01", gracePeriod = 0, movingAverage = "20", endDate = today.isoformat(), startingCash = 100000.00):
    #makes the dataset required for calculations
    Data_Creation.getStockData(tickerName, endDate= endDate)
    df = pd.read_csv(path + "\\" + tickerName + ".csv")

    #makes new dataframe with specified range
    mask =  (df["Date"] >= startDate) & (df["Date"] <= endDate)
    df2 = df.loc[mask]
    df2 = df2.reset_index(drop = True)

    #variables required for calculations
    stockPrice = round(df2["Open"][0], 2)
    cash = startingCash
    shares = int(startingCash/stockPrice)
    movingAveragePrice = 0.0
    gracePeriodCounter = 0
    marketValue = round(shares * stockPrice, 2)
    remainingCash = round(cash - marketValue, 2)
    action = "Buy"
    spreadSheet = {'Date': [startDate],
        'Price': [stockPrice],
        'Shares': [shares],
        'Market Value': [marketValue],
        'Remaining Amount': [remainingCash],
        'Total Amount': [cash],
        'Action': [action]
    }
    #iterate through the dataframe
    #for index in df2.index:
    for index in df2.index:
        stockPrice = round(df2["Open"][index], 2)
        oldMA = movingAveragePrice
        if movingAverage == "20":
            movingAveragePrice = round(df2['Twenty DMA'][index], 2)
        elif movingAverage == "50":
            movingAveragePrice = round(df2['Fifty DMA'][index], 2)
        else:
            print("Enter a valid moving day average")
            break
    #checks if something happens
        if (stockPrice < movingAveragePrice or movingAveragePrice < oldMA) and (action == "Buy"):
            gracePeriodCounter += 1
        elif (stockPrice > movingAveragePrice and movingAveragePrice > oldMA) and (action == "Sell"):
            gracePeriodCounter += 1
        else:
            gracePeriodCounter = 0
    #calls the buy or sell function if the condition is met
        if gracePeriodCounter > gracePeriod and action == "Buy":
            #sell shares
            marketValue = round(shares * stockPrice, 2)
            action = "Sell"
            cash = remainingCash + marketValue
            spreadSheet["Date"].append(df2['Date'][index])
            spreadSheet["Price"].append(stockPrice)
            spreadSheet["Shares"].append(shares)
            spreadSheet["Market Value"].append(marketValue)
            spreadSheet["Remaining Amount"].append(remainingCash)
            spreadSheet["Total Amount"].append(cash)
            spreadSheet["Action"].append(action)
        elif gracePeriodCounter > gracePeriod and action == "Sell":
            #buy shares
            shares = int(cash/stockPrice)
            marketValue = round(shares * stockPrice, 2)
            remainingCash = round(cash - marketValue, 2)
            action = "Buy"
            spreadSheet["Date"].append(df2['Date'][index])
            spreadSheet["Price"].append(stockPrice)
            spreadSheet["Shares"].append(shares)
            spreadSheet["Market Value"].append(marketValue)
            spreadSheet["Remaining Amount"].append(remainingCash)
            spreadSheet["Total Amount"].append(cash)
            spreadSheet["Action"].append(action)
    #save dictionary as csv
    endData = pd.DataFrame(spreadSheet, columns = ['Date', 'Price', 'Shares', 'Market Value', 'Remaining Amount', 'Total Amount', 'Action'])
    endData.to_csv(parentDir + "\\tradingData.csv")


ticker = input("Enter the Company you wish to Track: ")
startDate = input("Enter the Start Date in the format yy-mm-dd up to 1996-01-02. ex. 2005-03-23: ")
endDate = input('Enter the End Date in the format yy-mm-dd or leave empty for current date. ex. 2005-03-23: ')
gracePeriod = int(input("Enter the grace period from 0 to 15: "))
movingAvg = input("Enter the moving day average, either 20 or 50: ")


if endDate == '':
    startCalc(ticker, startDate, gracePeriod, movingAvg)
else:
    startCalc(ticker, startDate, gracePeriod, movingAvg, endDate)