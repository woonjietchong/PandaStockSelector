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

#debug mode
debug_mode = 0

#database variables
db_connected = False
conn = None
query = None
conn_target_path = r'klse_from_bursa.db'
entire_db_downloaded = 0
entire_db = None

def connect_to_database():
    global conn
    if not db_connected:
        conn = sqlite3.connect(conn_target_path)

def get_single_stock_db(stock_designated):
    global entire_db_downloaded
    global query
    global entire_db

    if debug_mode == 1:
        print("in get_single_stock_db")

    if entire_db_downloaded == 0:
        if debug_mode == 1:
            print("getting entire database")
        if not db_connected:
            connect_to_database()
        entire_db_query = "SELECT symbol,name,date_YYYY,date_MM,date_DD,close_price FROM stocks;"
        entire_db = pandas.read_sql_query(entire_db_query,conn)
        entire_db_downloaded = 1

    target_df = entire_db.loc[entire_db['symbol'] == stock_designated]
    target_df = target_df.sort_values(by=['date_YYYY','date_MM','date_DD'], ascending = True, inplace=False, kind='mergesort') #sort to calculate the rolling mean
    target_df = target_df.reset_index(drop=True) #rearrange index from 0,1,2,3......

    if debug_mode == 1:
        print(target_df)

    return target_df

def init_additional_fields_in_df(df):
    #Construct full date
    df = df.assign(Date="0")
    for i in range(df['symbol'].size):
        df.at[i, 'Date'] = str(df['date_YYYY'][i]).zfill(4) +"/"+str(df['date_MM'][i]).zfill(2) +"/"+str(df['date_DD'][i]).zfill(2)
    df['Date'] =  pandas.to_datetime(df['Date'], errors='raise', dayfirst=False, yearfirst=True)

    df = df.assign(ma20d=df.close_price)
    #df = df.assign(ma50d=df.close_price)
    df = df.assign(Bol_upper=df.close_price)
    df = df.assign(Bol_lower=df.close_price)
    #df = df.assign(Bol_BW=0.0)
    #df = df.assign(Bol_BW_200MA=0.0)
    #df = df.assign(exma20d=df.close_price)
    #df = df.assign(exma50d=df.close_price)
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
                #klse_single_stock_df = add_zero_padding_to_date_in_df(klse_single_stock_df)
                
                #klse_single_stock_df['Date'] =  pandas.to_datetime( klse_single_stock_df['Date'], errors='raise', dayfirst=False, yearfirst=True)
                #temp_data_set = klse_single_stock_df.sort_values(by='Date',ascending = True ) #sort to calculate the rolling mean
                temp_data_set = klse_single_stock_df

                temp_rolling_mean = klse_single_stock_df['close_price'].rolling(window=20).mean()
                temp_rolling_std = klse_single_stock_df['close_price'].rolling(window=20, min_periods=20).std()
                temp_data_set['ma20d'] = temp_rolling_mean
                #temp_data_set['ma50d'] = klse_single_stock_df['close_price'].rolling(window=50).mean()
                temp_data_set['Bol_upper'] = temp_rolling_mean + 2*temp_rolling_std
                temp_data_set['Bol_lower'] = temp_rolling_mean - 2*temp_rolling_std
                #temp_data_set['Bol_BW'] = ((klse_single_stock_df['Bol_upper'] - klse_single_stock_df['Bol_lower'])/klse_single_stock_df['ma20d'])*100
                #temp_data_set['Bol_BW_200MA'] = klse_single_stock_df['Bol_BW'].rolling(window=200).mean()
                #temp_data_set['Bol_BW_200MA'] = klse_single_stock_df['Bol_BW_200MA'].fillna(method='backfill')##?? ,may not be good
                #temp_data_set['exma20d'] = klse_single_stock_df['close_price'].ewm(span=20).mean()

                if debug_mode == 1:
                    print(temp_data_set)
                    print(temp_data_set['close_price'][temp_data_set['symbol'].size - 1])
                    print(temp_data_set['Bol_upper'][temp_data_set['symbol'].size - 1])

                if (temp_data_set['close_price'][temp_data_set['symbol'].size - 1] - temp_data_set['Bol_upper'][temp_data_set['symbol'].size - 1]) > 0.0001 :
                    print "----------------------------------------------------------------------------------------------------"
                    print "--------- found   " + temp_data_set['symbol'][0] + " " + temp_data_set['name'][0] + " matched-------"
                    temp_data_set.plot(x='Date', y=['close_price','ma20d','Bol_upper','Bol_lower' ])
                    plt.show()
                    print "----------------------------------------------------------------------------------------------------"
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