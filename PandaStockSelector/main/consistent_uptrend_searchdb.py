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

    if debug_mode == 1:
        print(target_df)

    return target_df

if __name__ == '__main__':
        start_searching = raw_input("Enter any text to start searching database: ")

        if start_searching != None:
            start_searching = True

            #retrive stock symbol from database
            print("---- reading database for symbols YYYY,MM,DD -----------")
            connect_to_database()
            stock_symbol_query =  "SELECT DISTINCT symbol FROM stocks"
            klse_stock_symbol_df = pandas.read_sql_query(stock_symbol_query,conn)

            stock_symbol_query =  "SELECT DISTINCT date_YYYY FROM stocks"
            klse_stock_date_YYYY_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_YYYY = int(klse_stock_date_YYYY_df['date_YYYY'][0])
            for i in range( klse_stock_date_YYYY_df['date_YYYY'].size):
                if int(klse_stock_date_YYYY_df['date_YYYY'][i]) > largest_date_YYYY:
                    largest_date_YYYY = int(klse_stock_date_YYYY_df['date_YYYY'][i])

            stock_symbol_query =  "SELECT DISTINCT date_MM FROM stocks WHERE date_YYYY = "+str(largest_date_YYYY)+";"
            klse_stock_date_MM_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_MM = int(klse_stock_date_MM_df['date_MM'][0])
            for i in range( klse_stock_date_MM_df['date_MM'].size):
                if int(klse_stock_date_MM_df['date_MM'][i]) > largest_date_MM:
                    largest_date_MM = int(klse_stock_date_MM_df['date_MM'][i])

            stock_symbol_query =  "SELECT DISTINCT date_DD FROM stocks WHERE date_YYYY = "+str(largest_date_YYYY)+" AND date_MM = "+str(largest_date_MM)+";"
            klse_stock_date_DD_df = pandas.read_sql_query(stock_symbol_query,conn)
            largest_date_DD = int(klse_stock_date_DD_df['date_DD'][0])
            for i in range( klse_stock_date_DD_df['date_DD'].size):
                if int(klse_stock_date_DD_df['date_DD'][i]) > largest_date_DD:
                    largest_date_DD = int(klse_stock_date_DD_df['date_DD'][i])
            print("------------  end of reading database --------")

            largest_date = str(largest_date_YYYY).zfill(4) +"-"+str(largest_date_MM).zfill(2) +"-"+str(largest_date_DD).zfill(2)

            if debug_mode == 1:
                print("largest_date = " + largest_date)

            klse_stock_symbol_df = klse_stock_symbol_df.assign(name="...")
            klse_stock_symbol_df = klse_stock_symbol_df.assign(uptrendfactor=0.0)

            if debug_mode == 1:
                print("---------------- klse_stock_symbol_df contains")
                print(klse_stock_symbol_df)
                print("---------------- klse_stock_symbol_df ends")

            for i in range(klse_stock_symbol_df['symbol'].size ):
                try:
                    uptrend_factor_sum = 0
                    uptrend_factor_avg = 0
                    calc_day_separation = 1
                    calc_cycle = 30
                    calc_num_of_calculations = calc_cycle * calc_day_separation

                    if debug_mode == 1:
                        print("----------------" + klse_stock_symbol_df['symbol'][i] + "----------------")

                    klse_single_stock_df = get_single_stock_db(klse_stock_symbol_df['symbol'][i])

                    temp_data_set = klse_single_stock_df.sort_values(by=['date_YYYY','date_MM','date_DD'],ascending = True ) #sort to calculate the rolling mean
                    temp_data_set = temp_data_set.reset_index(drop=True)
                    last_index = temp_data_set['symbol'].size - 1

                    if debug_mode == 1:
                        print("After sort dates")
                        print(temp_data_set)
                        print("calculating on " + (temp_data_set.tail(1))['symbol'])
                        print("size = " + str(temp_data_set['symbol'].size))
                        print((temp_data_set.tail(1))['close_price'])
                        print((temp_data_set.take([last_index]))['close_price'])

                    if (temp_data_set['symbol'].size > calc_num_of_calculations) and \
                    (temp_data_set['close_price'][last_index] > 0.50) and \
                    (temp_data_set['date_YYYY'][last_index] == largest_date_YYYY) and \
                    (temp_data_set['date_MM'][last_index] == largest_date_MM) and \
                    (temp_data_set['date_DD'][last_index] == largest_date_DD):
                        for j in range(calc_num_of_calculations):
                            uptrend_factor = (temp_data_set['close_price'][last_index - j] \
                            / (temp_data_set['close_price'][last_index - j - calc_day_separation]))
                            if uptrend_factor > 1.05: #Guard from extreme values
                                uptrend_factor = 1.05
                            uptrend_factor_sum = uptrend_factor_sum + uptrend_factor

                        uptrend_factor_avg = uptrend_factor_sum / calc_num_of_calculations

                        klse_stock_symbol_df.at[i, 'name'] = temp_data_set['name'][last_index]
                        klse_stock_symbol_df.at[i, 'uptrendfactor'] = uptrend_factor_avg
                    else:
                        if debug_mode == 1:
                            print("Calculating ...  Condition failed  ->"+str(temp_data_set['symbol'][last_index])+ " " +str(temp_data_set['name'][last_index]))
                            print("symbol size: " + str(temp_data_set['symbol'].size))
                            print("close price: " + str(temp_data_set['close_price'][last_index]))
                            print("year: " + str(temp_data_set['date_YYYY'][last_index]))
                            print("month: " + str(temp_data_set['date_MM'][last_index]))
                            print("date: " + str(temp_data_set['date_DD'][last_index]))
                except TypeError as current_error:
                    if debug_mode == 1:
                        print "TypeError, skip this stock " + str(current_error)
                    continue
                except KeyError as current_error:
                    if debug_mode == 1:
                        print "KeyError, skip this stock " + str(current_error)
                    continue
                except Exception as e:
                    if debug_mode == 1:
                        print "searching loop error: " + str(e)
                    continue

            #Sort and display the highest
            display_sorted_df = klse_stock_symbol_df.sort_values(by='uptrendfactor',ascending = False ) #sort to show highest uptrends
            print("Top 50 uptrend stock: ")
            print(display_sorted_df.head(50))

        end = raw_input("Enter any key to exit: ")
