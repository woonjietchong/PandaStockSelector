# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:53:47 2016

@author: vertwj

@brief analyze data in database and produce graphs

"""

#import os, re, sys, time, datetime, copy, shutil
import pandas
import sqlite3
#from yahoo_finance_historical_data_extract import YFHistDataExtr
import matplotlib.pyplot as plt
 
if __name__ == '__main__':
    
        print "-----------Showing plot------------------------"
        
        stock_designated = raw_input("Enter stock you want to analyse: ")
        
        if stock_designated != None:#== "searchdb":
            
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
            
            for i in range( klse_df['symbol'].size ):        
                try:
                    print "----------------" + klse_df['symbol'][i] + "----------------"
                    
                    print "---------------- pt 2 ----------------"
                    klse_df['Date'] =  pandas.to_datetime( klse_df['Date'], errors='raise', dayfirst=False, yearfirst=True)
                    temp_data_set = klse_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
                    
                    print "---------------- pt 3 ----------------"
                    temp_data_set['ma20d'] = pandas.rolling_mean(klse_df['close_price'], window=20)
                    temp_data_set['ma50d'] = pandas.rolling_mean(klse_df['close_price'], window=50)
                    temp_data_set['Bol_upper'] = pandas.rolling_mean(klse_df['close_price'], window=20) + 2* pandas.rolling_std(klse_df['close_price'], 20, min_periods=20)
                    temp_data_set['Bol_lower'] = pandas.rolling_mean(klse_df['close_price'], window=20) - 2* pandas.rolling_std(klse_df['close_price'], 20, min_periods=20)
                    temp_data_set['Bol_BW'] = ((klse_df['Bol_upper'] - klse_df['Bol_lower'])/klse_df['ma20d'])*100
                    temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(klse_df['Bol_BW'], window=50)#cant get the 200 daa
                    temp_data_set['Bol_BW_200MA'] = klse_df['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
                    temp_data_set['exma20d'] = pandas.ewma(klse_df['close_price'], span=20)
                    #temp_data_set['exma50d'] = pandas.ewma(temp_data_set['close_price'], span=50)
                     
                    #data_ext.all_stock_df.plot(x='Date', y=['close_price','ma20d','ma50d','Bol_upper','Bol_lower' ])
                    #data_ext.all_stock_df.plot(x='Date', y=['close_price','ma20d','Bol_upper','Bol_lower' ])
                    #data_ext.all_stock_df.plot(x='Date', y=['Bol_BW','Bol_BW_200MA' ])
                    
    
                    
    #                print "type of temp_data_set['close_price'] is " + str( type(temp_data_set['close_price']) )
    #                print "type of temp_data_set['Bol_upper'] is " + str( type(temp_data_set['Bol_upper']) )
    #                
    #                print  "temp_data_set['close_price'][0] is " + str( temp_data_set['close_price'][0] )
    #                print  "temp_data_set['Bol_upper'][0] is " + str( temp_data_set['Bol_upper'][0] )
                    
                    print "---------------- pt 4 ----------------"
                    print(temp_data_set)
                    if True:#temp_data_set['close_price'][0] > temp_data_set['Bol_upper'][0] :
                        print "------------------------------------------------------"
                        print "---------found   " + klse_df['name'][i] + " matched-------"
                        temp_data_set.plot(x='Date', y=['close_price','ma20d','Bol_upper','Bol_lower' ])
                        plt.show()
                        print "--------------------------------------------------------"
                except TypeError as current_error:
                    print "TypeError, skip this stock " + str( klse_df['symbol'][i] + " error: " + str(current_error))
                    continue
                except KeyError as current_error:
                    print "KeyError, skip this stock" + str( klse_df['symbol'][i] + " error: " + str(current_error))
                    continue
            
#        else:
#            data_ext = YFHistDataExtr()
#            data_ext.set_interval_to_retrieve(200)#in days
#            data_ext.set_multiple_stock_list([stock_designated])
#            data_ext.get_hist_data_of_all_target_stocks()
#            # convert the date column to date object
#            print data_ext.all_stock_df
#            #data_ext.all_stock_df[1] =  pandas.to_datetime( data_ext.all_stock_df[1])
#            data_ext.all_stock_df["Date"] =  pandas.to_datetime( data_ext.all_stock_df["Date"])
#            temp_data_set = data_ext.all_stock_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
#            
#            temp_data_set['ma20d'] = pandas.rolling_mean(temp_data_set['close_price'], window=20)
#            temp_data_set['ma50d'] = pandas.rolling_mean(temp_data_set['close_price'], window=50)
#            temp_data_set['Bol_upper'] = pandas.rolling_mean(temp_data_set['close_price'], window=20) + 2* pandas.rolling_std(temp_data_set['close_price'], 20, min_periods=20)
#            temp_data_set['Bol_lower'] = pandas.rolling_mean(temp_data_set['close_price'], window=20) - 2* pandas.rolling_std(temp_data_set['close_price'], 20, min_periods=20)
#            temp_data_set['Bol_BW'] = ((temp_data_set['Bol_upper'] - temp_data_set['Bol_lower'])/temp_data_set['ma20d'])*100
#            temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(temp_data_set['Bol_BW'], window=50)#cant get the 200 daa
#            temp_data_set['Bol_BW_200MA'] = temp_data_set['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
#            temp_data_set['exma20d'] = pandas.ewma(temp_data_set['close_price'], span=20)
#            temp_data_set['exma50d'] = pandas.ewma(temp_data_set['close_price'], span=50)
#            data_ext.all_stock_df = temp_data_set.sort('Date',ascending = False ) #revese back to original
#             
#            data_ext.all_stock_df.plot(x='Date', y=['close_price','ma20d','ma50d','Bol_upper','Bol_lower' ])
#            data_ext.all_stock_df.plot(x='Date', y=['Bol_BW','Bol_BW_200MA' ])
#            
#            plt.show()
        
        end = raw_input("Enter any key to exit: ")