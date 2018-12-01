#!/usr/bin/python
# -*- coding: iso-8859-1 -*-
# Input into database from file

from tika import parser
import re
import sqlite3

if __name__ == "__main__":
        input_file = raw_input("Enter input file: ")
        print("raw data is in processing")
        parsedPDF = parser.from_file(input_file) #old code ("C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\securities_equities_300418.pdf")
        parsedContent = parsedPDF["content"]
        
        
        # remove ','
        translation = {44: None}
        parsedContent = parsedContent.translate(translation) 

        regexMatches = re.findall(r"([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) ([0-9][0-9][0-9][0-9][A-Z0-9]??[A-Z0-9]??) (.*) MYR (.*) (.*) (.*) (.*) (.*) (.*)", parsedContent)

        #for groupsInRegex in regexMatches:            
            #print("----------")
            #print(groupsInRegex[0]) #--> Date
            #print(groupsInRegex[1]) #--> Month
            #print(groupsInRegex[2]) #--> Year
            #print(groupsInRegex[3]) #--> Stock Code
            #print(groupsInRegex[4]) #--> Stock Name
            #print(groupsInRegex[5]) #--> Opening Price
            #print(groupsInRegex[6]) #--> High Price
            #print(groupsInRegex[7]) #--> Low Price
            #print(groupsInRegex[8]) #--> Closing Price
            #print(groupsInRegex[9]) #--> Volume Traded
            #print(groupsInRegex[10]) #--> Value Traded
            #print("----------")
            
        print("Starting wj stock db input")
        conn = sqlite3.connect('klse_from_bursa.db')
        conn_closed = False
        print("after conn connect")
        try:
            c = conn.cursor()
            print("after conn.cursor")
    
            # Create table
            # Database Schema
            #   symbol	            TEXT
            #   name                TEXT
            #   date-YYYY	        INTEGER
            #   date-MM             INTEGER
            #   date-DD             INTEGER
            #   open_price          NUMERIC -> decimal 3, 2
            #   high_price          NUMERIC -> decimal 3, 2
            #   low_price	        NUMERIC -> decimal 3, 2
            #   close_price	        NUMERIC -> decimal 3, 2
            #   volume	            INTEGER -> unsigned bigInt
            #   value_traded	      INTEGER -> unsigned bigInt
            
            c.execute('''CREATE TABLE IF NOT EXISTS stocks (symbol text, name text, date_YYYY integer, date_MM integer, date_DD integer, open_price numeric, high_price numeric, low_price numeric, close_price numeric, volume integer, value_traded integer)''')
            print("after CREATE TABLE")
            
            for groupsInRegex in regexMatches:
                current_stock_symbol = groupsInRegex[3]                  #TEXT
                current_stock_name = groupsInRegex[4]                    #TEXT
                current_stock_date_YYYY	= groupsInRegex[2]          #INTEGER
                current_stock_date_MM = groupsInRegex[1]            #INTEGER
                current_stock_date_DD = groupsInRegex[0]            #INTEGER
                
                try:
                    current_stock_open_price = str(float(groupsInRegex[5]))         #NUMERIC -> decimal 3, 2
                except Exception, e:
                    print(current_stock_name + " conversion failure")
                    print(e)
                    current_stock_open_price = "0.0"
                
                try:
                    current_stock_high_price = str(float(groupsInRegex[6]))        #NUMERIC -> decimal 3, 2
                except Exception, e:
                    print(current_stock_name + " conversion failure")
                    print(e)
                    current_stock_high_price = "0.0"
                    
                try:
                    current_stock_low_price	= str(float(groupsInRegex[7]))        #NUMERIC -> decimal 3, 2
                    #print("after get_days_low")
                except Exception, e:
                    print(current_stock_name + " conversion failure")
                    print(e)
                    current_stock_low_price = "0.0"
                    
                try:
                    current_stock_close_price = str(float(groupsInRegex[8]))	      #NUMERIC -> decimal 3, 2
                    #print("after get_price")
                except Exception, e:
                    print(current_stock_name + " conversion failure")
                    print(e)
                    current_stock_close_price = "0.0"

                current_stock_volume = groupsInRegex[9]	           #INTEGER -> unsigned bigInt
                current_stock_value_traded = groupsInRegex[10]	      #INTEGER -> unsigned bigInt
                
                #First
                db_query_string = "INSERT INTO stocks VALUES (" + "'" + current_stock_symbol + "'" 
                db_query_string = db_query_string + ", " + "'" + current_stock_name + "'"
                db_query_string = db_query_string + ", " + current_stock_date_YYYY
                db_query_string = db_query_string + ", " + current_stock_date_MM
                db_query_string = db_query_string + ", " + current_stock_date_DD                   
                db_query_string = db_query_string + ", " + current_stock_open_price
                db_query_string = db_query_string + ", " + current_stock_high_price
                db_query_string = db_query_string + ", " + current_stock_low_price
                db_query_string = db_query_string + ", " + current_stock_close_price
                db_query_string = db_query_string + ", " + current_stock_volume
                db_query_string = db_query_string + ", " + current_stock_value_traded

                #Last                
                db_query_string = db_query_string +")"
                
                try:
                    # Insert a row of data
                    c.execute(db_query_string)
                except Exception, e:
                    print("Query Execution failure")
                    print(db_query_string)
                    print(e)
                    

            # Save (commit) the changes
            print("Saving changes to database")
            conn.commit()
            
        except Exception, e:
            #cleanup to prevent database not accessible later
            print("General database failure , now cleanup")
            print(e)
            conn.close()
            conn_closed = True
        
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        if(not conn_closed):
            print("Closing connection")
            conn.close()
