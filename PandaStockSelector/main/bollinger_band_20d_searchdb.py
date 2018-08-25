# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 11:29:48 2018

@author: vertwj

@brief search database and find bollinger breakouts

"""

#import os, re, sys, time, datetime, copy, shutil
import pandas
import sqlite3
import matplotlib.pyplot as plt

#database variables
db_connected = False
conn = None
query = None
conn_target_path = 'C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\klse_from_bursa.db'

def connect_to_database():
    global conn
    if not db_connected:
        conn = sqlite3.connect(conn_target_path)

def get_single_stock_db(stock_designated):
    #print "in get_single_stock_db"
    global query
    
    #append ' ' to stock_designated to prevent database error
    stock_designated = "'" + stock_designated + "'"
    
    if not db_connected:    
        connect_to_database()
    query = "SELECT symbol,name,date_YYYY,date_MM,date_DD,open_price,high_price,low_price,close_price,volume,value_traded FROM stocks WHERE symbol = " + stock_designated + ";"
    target_df = pandas.read_sql_query(query,conn)
    return target_df
    
def add_zero_padding_to_date_in_df(df):
    #Init date column in dataframe
    #print("--- add_zero_padding_to_date_in_df---------------- df contains")
    #print df
    #print("--- add_zero_padding_to_date_in_df---------------- df ends")
            
    for i in range( df['symbol'].size ):        
        try:
            #print "----------------" + df['symbol'][i] + "-- construct date ----------------"
            #print(df['date_YYYY'][i])
            #print(df['date_MM'][i])
            #print(df['date_DD'][i])
            #print(str(df['date_YYYY'][i])+"/"+str(df['date_MM'][i])+"/"+str(df['date_DD'][i]))
            df.iat[i,11] = str(df['date_YYYY'][i]).zfill(4) +"/"+str(df['date_MM'][i]).zfill(2) +"/"+str(df['date_DD'][i]).zfill(2)
        except Exception as e:
            print "error in add_zero_padding_to_date_in_df for loop " + str(e)
                    
    #print("--- add_zero_padding_to_date_in_df---------------- df contains")
    #print df
    #print("--- add_zero_padding_to_date_in_df---------------- df ends")
    return df
    
def init_additional_fields_in_df(df):
    df = df.assign(Date="0")
    df = df.assign(ma20d=df.close_price)
    df = df.assign(ma50d=df.close_price)
    df = df.assign(Bol_upper=df.close_price)
    df = df.assign(Bol_lower=df.close_price)
    df = df.assign(Bol_BW=0.0)
    df = df.assign(Bol_BW_200MA=0.0)
    df = df.assign(exma20d=df.close_price)
    df = df.assign(exma50d=df.close_price)
    return df

if __name__ == '__main__':
    
        print "-----------Showing plot------------------------"
        
        start_searching = raw_input("Enter any text to start searching database: ")
        
        if start_searching != None:
            start_searching = True
            
            #retrive stock symbol from database
            print("---------------- reading database")
            connect_to_database()
            stock_symbol_query =  "SELECT DISTINCT symbol FROM stocks"
            #stock_symbol_query =  "SELECT DISTINCT symbol FROM stocks WHERE symbol = 2089;"            
            klse_stock_symbol_df = pandas.read_sql_query(stock_symbol_query,conn)
            print("---------------- end of reading database")

            print("---------------- klse_stock_symbol_df contains")
            print klse_stock_symbol_df
            print("---------------- klse_stock_symbol_df ends")
            
            for i in range( klse_stock_symbol_df['symbol'].size ):        
                try:
                    #print "----------------" + klse_stock_symbol_df['symbol'][i] + "----------------"
                    klse_single_stock_df = get_single_stock_db(klse_stock_symbol_df['symbol'][i])
                    
                    #init empty values
                    klse_single_stock_df = init_additional_fields_in_df(klse_single_stock_df)
                    klse_single_stock_df = add_zero_padding_to_date_in_df(klse_single_stock_df)
                    
                    klse_single_stock_df['Date'] =  pandas.to_datetime( klse_single_stock_df['Date'], errors='raise', dayfirst=False, yearfirst=True)
                    temp_data_set = klse_single_stock_df.sort('Date',ascending = True ) #sort to calculate the rolling mean
                    
                    temp_data_set['ma20d'] = pandas.rolling_mean(klse_single_stock_df['close_price'], window=20)
                    temp_data_set['ma50d'] = pandas.rolling_mean(klse_single_stock_df['close_price'], window=50)
                    temp_data_set['Bol_upper'] = pandas.rolling_mean(klse_single_stock_df['close_price'], window=20) + 2* pandas.rolling_std(klse_single_stock_df['close_price'], 20, min_periods=20)
                    temp_data_set['Bol_lower'] = pandas.rolling_mean(klse_single_stock_df['close_price'], window=20) - 2* pandas.rolling_std(klse_single_stock_df['close_price'], 20, min_periods=20)
                    temp_data_set['Bol_BW'] = ((klse_single_stock_df['Bol_upper'] - klse_single_stock_df['Bol_lower'])/klse_single_stock_df['ma20d'])*100
                    temp_data_set['Bol_BW_200MA'] = pandas.rolling_mean(klse_single_stock_df['Bol_BW'], window=50)#cant get the 200 daa
                    temp_data_set['Bol_BW_200MA'] = klse_single_stock_df['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
                    temp_data_set['exma20d'] = pandas.ewma(klse_single_stock_df['close_price'], span=20)
            
                    #print(temp_data_set)
                    #print(temp_data_set['close_price'][temp_data_set['symbol'].size - 1])
                    #print(temp_data_set['Bol_upper'][temp_data_set['symbol'].size - 1])
                    if (temp_data_set['close_price'][temp_data_set['symbol'].size - 1] - temp_data_set['Bol_upper'][temp_data_set['symbol'].size - 1]) > 0.0001 :
                        print "------------------------------------------------------"
                        print "---------found   " + temp_data_set['symbol'][0] + " " + temp_data_set['name'][0] + " matched-------"
                        temp_data_set.plot(x='Date', y=['close_price','ma20d','Bol_upper','Bol_lower' ])
                        plt.show()
                        print "--------------------------------------------------------"
                except TypeError as current_error:
                    print "TypeError, skip this stock " + str( klse_stock_symbol_df['symbol'][i] + " error: " + str(current_error))
                    continue
                except KeyError as current_error:
                    print "KeyError, skip this stock " + str( klse_stock_symbol_df['symbol'][i] + " error: " + str(current_error))
                    continue
                except Exception as e:
                    print "searching loop error: " + str(e)
                    continue
        
        end = raw_input("Enter any key to exit: ")