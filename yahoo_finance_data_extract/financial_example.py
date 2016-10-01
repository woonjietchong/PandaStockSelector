# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:53:47 2016

@author: Admin
"""

import os, re, sys, time, datetime, copy, shutil
import pandas
from yahoo_finance_historical_data_extract import YFHistDataExtr
import matplotlib.pyplot as plt
 
if __name__ == '__main__':
    
        print "-----------Showing plot------------------------"
        
        
        
        stock_designated = raw_input("Enter stock you want to analyse: ")
        
        if stock_designated == "searchdb":
            
            klse_df = pandas.read_csv('klse_stocks_25_09_2016.csv')     
            
            print klse_df
            
            #retrive database from text file
        
            number_of_stocks = raw_input("Enter number of stock you want to analyse: ")

            stocks_array = []
            for i in range( int(number_of_stocks) ):
                entered_stock_code = raw_input("Enter stock code ["+str(i)+"] :" )
                stocks_array.append(entered_stock_code)
                
            print stocks_array
            
            
            
            for i in range( int(number_of_stocks) ):
                
                print "----------------" + stocks_array[i] + "----------------"
                data_ext = YFHistDataExtr()
                data_ext.set_interval_to_retrieve(200)#in days
                data_ext.set_multiple_stock_list([stocks_array[i]])
                data_ext.get_hist_data_of_all_target_stocks()
                # convert the date column to date object
                data_ext.all_stock_df['Date'] =  pandas.to_datetime( data_ext.all_stock_df['Date'])
                temp_data_set = data_ext.all_stock_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
                
                temp_data_set['20d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20)
                temp_data_set['50d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=50)
                temp_data_set['Bol_upper'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) + 2* pandas.rolling_std(temp_data_set['Adj Close'], 20, min_periods=20)
                temp_data_set['Bol_lower'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) - 2* pandas.rolling_std(temp_data_set['Adj Close'], 20, min_periods=20)
                temp_data_set['Bol_BW'] = ((temp_data_set['Bol_upper'] - temp_data_set['Bol_lower'])/temp_data_set['20d_ma'])*100
                temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(temp_data_set['Bol_BW'], window=50)#cant get the 200 daa
                temp_data_set['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
                temp_data_set['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
                #temp_data_set['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)
                data_ext.all_stock_df = temp_data_set.sort('Date',ascending = False ) #revese back to original
                 
                #data_ext.all_stock_df.plot(x='Date', y=['Adj Close','20d_ma','50d_ma','Bol_upper','Bol_lower' ])
                data_ext.all_stock_df.plot(x='Date', y=['Adj Close','20d_ma','Bol_upper','Bol_lower' ])
                #data_ext.all_stock_df.plot(x='Date', y=['Bol_BW','Bol_BW_200MA' ])
                
                print temp_data_set['Adj Close']
                print temp_data_set['Bol_upper']
                
                print "type of temp_data_set['Adj Close'] is " + str( type(temp_data_set['Adj Close']) )
                print "type of temp_data_set['Bol_upper'] is " + str( type(temp_data_set['Bol_upper']) )
                
                print  "temp_data_set['Adj Close'][0] is " + str( temp_data_set['Adj Close'][0] )
                print  "temp_data_set['Bol_upper'][0] is " + str( temp_data_set['Bol_upper'][0] )             
                
                plt.show()
                
                print "--------------------------------------------------------"
            
        else:
            data_ext = YFHistDataExtr()
            data_ext.set_interval_to_retrieve(200)#in days
            data_ext.set_multiple_stock_list([stock_designated])
            data_ext.get_hist_data_of_all_target_stocks()
            # convert the date column to date object
            data_ext.all_stock_df['Date'] =  pandas.to_datetime( data_ext.all_stock_df['Date'])
            temp_data_set = data_ext.all_stock_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
            
            temp_data_set['20d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20)
            temp_data_set['50d_ma'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=50)
            temp_data_set['Bol_upper'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) + 2* pandas.rolling_std(temp_data_set['Adj Close'], 20, min_periods=20)
            temp_data_set['Bol_lower'] = pandas.rolling_mean(temp_data_set['Adj Close'], window=20) - 2* pandas.rolling_std(temp_data_set['Adj Close'], 20, min_periods=20)
            temp_data_set['Bol_BW'] = ((temp_data_set['Bol_upper'] - temp_data_set['Bol_lower'])/temp_data_set['20d_ma'])*100
            temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(temp_data_set['Bol_BW'], window=50)#cant get the 200 daa
            temp_data_set['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
            temp_data_set['20d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=20)
            temp_data_set['50d_exma'] = pandas.ewma(temp_data_set['Adj Close'], span=50)
            data_ext.all_stock_df = temp_data_set.sort('Date',ascending = False ) #revese back to original
             
            data_ext.all_stock_df.plot(x='Date', y=['Adj Close','20d_ma','50d_ma','Bol_upper','Bol_lower' ])
            data_ext.all_stock_df.plot(x='Date', y=['Bol_BW','Bol_BW_200MA' ])
            
            plt.show()
        
        end = raw_input("Enter any key to exit: ")