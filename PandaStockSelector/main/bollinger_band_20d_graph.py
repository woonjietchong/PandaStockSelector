# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 10:59:24 2018

@author: Admin
@brief analyze data in database and produce graphs
"""

import pandas
import sqlite3
import matplotlib.pyplot as plt
 
if __name__ == '__main__':
    stock_designated = raw_input("Enter stock you want to analyse: ")
    
    if stock_designated != None:
        
        #retrive database from text file
        print("---------------- reading database")
        conn = sqlite3.connect('C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\klse_from_bursa_dup.db')
        query = "SELECT symbol,name,date_YYYY,date_MM,date_DD,open_price,high_price,low_price,close_price,volume,value_traded FROM stocks WHERE symbol = " + stock_designated #3301"
 
        klse_df = pandas.read_sql_query(query,conn)
        print("---------------- end of reading database")
        
        #Init date column in dataframe
        klse_df = klse_df.assign(Date="0")
        klse_df = klse_df.assign(ma20d=klse_df.close_price)
        klse_df = klse_df.assign(ma50d=klse_df.close_price)
        klse_df = klse_df.assign(Bol_upper=klse_df.close_price)
        klse_df = klse_df.assign(Bol_lower=klse_df.close_price)
        klse_df = klse_df.assign(Bol_BW=0.0)
        klse_df = klse_df.assign(Bol_BW_200MA=0.0)
        klse_df = klse_df.assign(exma20d=klse_df.close_price)
        klse_df = klse_df.assign(exma50d=klse_df.close_price)
        
        #Init date array
        klse_df_date_arr = []
        
        print("---------------- klse_df contains")
        print klse_df
        
        
        #print klse_df['symbol'].size
        print klse_df['symbol'].size
        
        for i in range( klse_df['symbol'].size ):        
            try:
                print "----------------" + klse_df['symbol'][i] + "-- construct date ----------------"
                print(klse_df['date_YYYY'][i])
                print(klse_df['date_MM'][i])
                print(klse_df['date_DD'][i])
                print(str(klse_df['date_YYYY'][i])+"/"+str(klse_df['date_MM'][i])+"/"+str(klse_df['date_DD'][i]))
                klse_df_date_arr.append(str(klse_df['date_YYYY'][i]).zfill(4) +"/"+str(klse_df['date_MM'][i]).zfill(2) +"/"+str(klse_df['date_DD'][i]).zfill(2) )
                klse_df.iat[i,11] = str(klse_df['date_YYYY'][i]).zfill(4) +"/"+str(klse_df['date_MM'][i]).zfill(2) +"/"+str(klse_df['date_DD'][i]).zfill(2)
                print(klse_df_date_arr)
            except TypeError as current_error:
                print(current_error)
                
        print klse_df
        
        for i in range( 1 ):        
            try:
                print "----------------" + klse_df['symbol'][i] + "----------------"
                klse_df['Date'] =  pandas.to_datetime( klse_df['Date'], errors='raise', dayfirst=False, yearfirst=True)
                temp_data_set = klse_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
                
                temp_data_set['ma20d'] = pandas.rolling_mean(klse_df['close_price'], window=20)
                temp_data_set['ma50d'] = pandas.rolling_mean(klse_df['close_price'], window=50)
                temp_data_set['Bol_upper'] = pandas.rolling_mean(klse_df['close_price'], window=20) + 2* pandas.rolling_std(klse_df['close_price'], 20, min_periods=20)
                temp_data_set['Bol_lower'] = pandas.rolling_mean(klse_df['close_price'], window=20) - 2* pandas.rolling_std(klse_df['close_price'], 20, min_periods=20)
                temp_data_set['Bol_BW'] = ((klse_df['Bol_upper'] - klse_df['Bol_lower'])/klse_df['ma20d'])*100
                temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(klse_df['Bol_BW'], window=50)#cant get the 200 daa
                temp_data_set['Bol_BW_200MA'] = klse_df['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
                temp_data_set['exma20d'] = pandas.ewma(klse_df['close_price'], span=20)
                
                print(temp_data_set)
                if True:
                    temp_data_set.plot(x='Date', y=['close_price','ma20d','Bol_upper','Bol_lower' ])
                    plt.show()
            except TypeError as current_error:
                print "TypeError, skip this stock " + str( klse_df['symbol'][i] + " error: " + str(current_error))
                continue
            except KeyError as current_error:
                print "KeyError, skip this stock" + str( klse_df['symbol'][i] + " error: " + str(current_error))
                continue
    
    end = raw_input("Enter any key to exit: ")