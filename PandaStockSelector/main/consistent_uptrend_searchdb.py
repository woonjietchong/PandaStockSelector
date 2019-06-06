# -*- coding: utf-8 -*-
"""
Created on Sun Jan 13 13:55:48 2019

@author: vertwj

@brief search database and find consistent trends

"""

import pandas
import sqlite3

#debug mode
debug_mode = 0

#database variables
db_connected = False
conn = None
query = None
conn_target_path = r'C:\Users\vertw\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\klse_from_bursa.db'

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
            klse_stock_symbol_df = pandas.read_sql_query(stock_symbol_query,conn)

            connect_to_database()
            stock_symbol_query =  "SELECT DISTINCT date_YYYY FROM stocks"
            klse_stock_date_YYYY_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_YYYY = int(klse_stock_date_YYYY_df['date_YYYY'][0])
            for i in range( klse_stock_date_YYYY_df['date_YYYY'].size):
                if int(klse_stock_date_YYYY_df['date_YYYY'][i]) > largest_date_YYYY:
                    largest_date_YYYY = int(klse_stock_date_YYYY_df['date_YYYY'][i])

            connect_to_database()
            stock_symbol_query =  "SELECT DISTINCT date_MM FROM stocks WHERE date_YYYY = "+str(largest_date_YYYY)+";"
            klse_stock_date_MM_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_MM = int(klse_stock_date_MM_df['date_MM'][0])
            for i in range( klse_stock_date_MM_df['date_MM'].size):
                if int(klse_stock_date_MM_df['date_MM'][i]) > largest_date_MM:
                    largest_date_MM = int(klse_stock_date_MM_df['date_MM'][i])

            connect_to_database()
            stock_symbol_query =  "SELECT DISTINCT date_DD FROM stocks WHERE date_YYYY = "+str(largest_date_YYYY)+" AND date_MM = "+str(largest_date_MM)+";"
            klse_stock_date_DD_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_DD = int(klse_stock_date_DD_df['date_DD'][0])
            for i in range( klse_stock_date_DD_df['date_DD'].size):
                if int(klse_stock_date_DD_df['date_DD'][i]) > largest_date_DD:
                    largest_date_DD = int(klse_stock_date_DD_df['date_DD'][i])
            print("---------------- end of reading database")

            if debug_mode == 1:
                print "largest_date_YYYY = " + str(largest_date_YYYY)
                print "largest_date_MM = " + str(largest_date_MM)
                print "largest_date_DD = " + str(largest_date_DD)
            largest_date = str(largest_date_YYYY).zfill(4) +"-"+str(largest_date_MM).zfill(2) +"-"+str(largest_date_DD).zfill(2)
            
            klse_stock_symbol_df = klse_stock_symbol_df.assign(ma20d=0)
            klse_stock_symbol_df = klse_stock_symbol_df.assign(ma50d=0)
            klse_stock_symbol_df = klse_stock_symbol_df.assign(vol5d=0)
            klse_stock_symbol_df = klse_stock_symbol_df.assign(name="...")
            klse_stock_symbol_df = klse_stock_symbol_df.assign(uptrendfactor=0.0)

            if debug_mode == 1:
                print("---------------- klse_stock_symbol_df contains")
                print(klse_stock_symbol_df)
                print("---------------- klse_stock_symbol_df ends")
            
            for i in range(klse_stock_symbol_df['symbol'].size ):        
                try:
                    if debug_mode == 1:
                        print "----------------" + klse_stock_symbol_df['symbol'][i] + "----------------"

                    klse_single_stock_df = get_single_stock_db(klse_stock_symbol_df['symbol'][i])
                    
                    #init empty values
                    klse_single_stock_df = init_additional_fields_in_df(klse_single_stock_df)
                    klse_single_stock_df = add_zero_padding_to_date_in_df(klse_single_stock_df)
                    uptrend_factor_sum = 0
                    uptrend_factor_avg = 0
                    calc_day_separation = 1
                    calc_cycle = 30
                    calc_num_of_calculations = calc_cycle * calc_day_separation
                    
                    klse_single_stock_df['Date'] =  pandas.to_datetime( klse_single_stock_df['Date'], errors='raise', dayfirst=False, yearfirst=True)
                    
                    temp_data_set = klse_single_stock_df.sort_values(by='Date',ascending = True ) #sort to calculate the rolling mean

                    if debug_mode == 1:
                        print klse_single_stock_df['Date'][klse_single_stock_df['symbol'].size - 1]
                        print str(temp_data_set['Date'][temp_data_set['symbol'].size - 1])
    
                    if temp_data_set['symbol'].size > calc_num_of_calculations and \
                    temp_data_set['close_price'][temp_data_set['symbol'].size - 1] > 1.00 and \
                    ((str(temp_data_set['Date'][temp_data_set['symbol'].size - 1]).find(largest_date)) != -1):
                        print "calculating on " + temp_data_set['symbol'][0]
                        print "size = " + str(temp_data_set['symbol'].size)
                        for j in range(calc_num_of_calculations):
                            uptrend_factor = (temp_data_set['close_price'][temp_data_set['symbol'].size - 1 - j] \
                            / temp_data_set['close_price'][temp_data_set['symbol'].size - 1 - j - calc_day_separation])
                            if uptrend_factor > 1.10: #Guard from extreme values
                                uptrend_factor = 1.10
                            uptrend_factor_sum = uptrend_factor_sum + uptrend_factor
                        
                        uptrend_factor_avg = uptrend_factor_sum / calc_num_of_calculations
                        klse_stock_symbol_df['name'][i] = temp_data_set['name'][0]
                        klse_stock_symbol_df['uptrendfactor'][i] = uptrend_factor_avg
                except TypeError as current_error:
                    print "TypeError, skip this stock " + str(current_error)
                    continue
                except KeyError as current_error:
                    print "KeyError, skip this stock " + str(current_error)
                    continue
                except Exception as e:
                    print "searching loop error: " + str(e)
                    continue

            #Sort and display the highest
            display_sorted_df = klse_stock_symbol_df.sort_values(by='uptrendfactor',ascending = False ) #sort to show highest uptrends
            #i = 0
            print("Sorted highest uptrend: " + str(display_sorted_df))
            #print(display_sorted_df.iloc[i,:])
            #i = i+1
            #print(display_sorted_df.iloc[i,:])

        end = raw_input("Enter any key to exit: ")
