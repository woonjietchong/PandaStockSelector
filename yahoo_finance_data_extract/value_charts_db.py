from yahoo_finance import Share
import sqlite3
import csv

#----- Globals variables ----------
stock_symbols = []
stock_symbol_reader = None
conn_closed = False

#Constants
CHAR_SHORTFORM_OF_MILLION = 'M'
VALUE_OF_MILLION = 1000000
CHAR_SHORTFORM_OF_BILLION = 'B'
VALUE_OF_BILLION = 1000000000
#----- End of Globals variables ---

# Helper function to convert yahoo finance get_market_cap() return string
# to float point numbers
# Or else SQL query will fail
# e.g., "35.56M" string to 35560000(float)
def convert_string_M_B_to_real(market_cap_text):
    try:
        if(market_cap_text[-1] == CHAR_SHORTFORM_OF_MILLION):
            print "CHAR_SHORTFORM_OF_MILLION"
            new_market_cap_text = market_cap_text[ 0 : (len(market_cap_text)-1) ]
            print "    " + new_market_cap_text
            float_market_cap = float(new_market_cap_text)
            print "    " + str(float_market_cap)
            float_market_cap = float_market_cap * VALUE_OF_MILLION
            print "    " + str(float_market_cap)
            return float_market_cap
        elif(market_cap_text[-1] == CHAR_SHORTFORM_OF_BILLION):
            print "CHAR_SHORTFORM_OF_BILLION"
            new_market_cap_text = market_cap_text[ 0 : (len(market_cap_text)-1) ]
            float_market_cap = float(new_market_cap_text)
            float_market_cap = float_market_cap * VALUE_OF_BILLION
            return float_market_cap
        else: #No conversion needed
            float_market_cap = float(market_cap_text)
            return float_market_cap
    except:
        print "market_cap_to_real failure"
        return market_cap_text

###### Main function ########################
if __name__ == '__main__':
    print "Starting wj stock db collection"
    csvfile = open('klse_stocks_26_06_2017_for_db.csv', 'rb')
    #with open('klse_stocks_25_09_2016.csv', 'rb') as csvfile:
    stock_symbol_reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for iterated_symbol in stock_symbol_reader:
        #print ' -+- '.join(iterated_symbol)
        #Use [0] to access inners value as iterated_symbol is like ['7036.KL']
        stock_symbols.append(iterated_symbol[0]) 
        
            
    #print stock_symbols
            
    
    conn = sqlite3.connect('klse_stocks_from_yahoo_finance.db')
    print "after conn connect"
    try:
        c = conn.cursor()
        print "after conn.cursor"

        # Create table
        # Database Schema
        #   symbol	            TEXT
        #   name                TEXT
        #   date-YYYY	        INTEGER
        #   date-MM             INTEGER
        #   date-DD             INTEGER
        #   date_in_full_string	TEXT
        #   open_price          NUMERIC -> decimal 3, 2
        #   high_price          NUMERIC -> decimal 3, 2
        #   low_price	        NUMERIC -> decimal 3, 2
        #   close_price	        NUMERIC -> decimal 3, 2
        #   volume	            INTEGER -> unsigned bigInt
        #   ebitda	            REAL
        #   market_cap	        REAL
        
        #c.execute('''CREATE TABLE IF NOT EXISTS stocks (symbol text, date text, price real)''')
        c.execute('''CREATE TABLE IF NOT EXISTS stocks (symbol text, name text, date_YYYY integer, date_MM integer, date_DD integer, date_in_full_string text, open_price numeric, high_price numeric, low_price numeric, close_price numeric, volume integer, ebitda real, market_cap real)''')
        print "after CREATE TABLE"
        
        print "getting finance data from yahoo"
        for iterated_symbol in stock_symbols:
            print iterated_symbol
            current_stock = Share(iterated_symbol)
            
            try:
                current_stock_symbol = iterated_symbol
                current_stock_name = current_stock.get_name()               #TEXT
                
                temp_trade_datetime = current_stock.get_trade_datetime()	#TEXT
                  # for future reference : example of get_trade_datetime() are 2017-06-23 20:17:00 UTC+0000
                current_stock_date_YYYY	= temp_trade_datetime[0:4]        #INTEGER
                current_stock_date_MM = temp_trade_datetime[5:7]            #INTEGER
                current_stock_date_DD = temp_trade_datetime[8:10]            #INTEGER
                current_stock_date_in_full_string = temp_trade_datetime
                
                current_stock_open_price = current_stock.get_open()         #NUMERIC -> decimal 3, 2
                print "after get_open"
                current_stock_high_price = current_stock.get_days_high()         #NUMERIC -> decimal 3, 2
                print "after get_days_high"
                current_stock_low_price	= current_stock.get_days_low()        #NUMERIC -> decimal 3, 2
                print "after get_days_low"
                current_stock_close_price = current_stock.get_price()	        #NUMERIC -> decimal 3, 2
                print "after get_price"
                current_stock_volume = current_stock.get_volume()	            #INTEGER -> unsigned bigInt
                print "after get_volume"
                temp_ebitda = current_stock.get_ebitda()	            #REAL
                current_stock_ebitda = str(convert_string_M_B_to_real(temp_ebitda))
                print "after get_ebitda"
                temp_market_cap = current_stock.get_market_cap()	        #REAL
                current_stock_market_cap = str(convert_string_M_B_to_real(temp_market_cap))
                print "after market_cap_to_real"
                
                #First
                db_query_string = "INSERT INTO stocks VALUES (" + "'" + current_stock_symbol + "'" 
                print "after first"
                db_query_string = db_query_string + ", " + "'" + current_stock_name + "'"
                db_query_string = db_query_string + ", " + current_stock_date_YYYY
                db_query_string = db_query_string + ", " + current_stock_date_MM
                db_query_string = db_query_string + ", " + current_stock_date_DD                   
                db_query_string = db_query_string + ", " + "'" + current_stock_date_in_full_string + "'"
                db_query_string = db_query_string + ", " + current_stock_open_price
                db_query_string = db_query_string + ", " + current_stock_high_price
                db_query_string = db_query_string + ", " + current_stock_low_price
                db_query_string = db_query_string + ", " + current_stock_close_price
                db_query_string = db_query_string + ", " + current_stock_volume
                db_query_string = db_query_string + ", " + current_stock_ebitda
                db_query_string = db_query_string + ", " + current_stock_market_cap

                #Last                
                db_query_string = db_query_string +")"
    
                print db_query_string
                query_string_construct_success = True
            except Exception, e:
                print e
                query_string_construct_success = False
                
            try:
                if(query_string_construct_success):
                    # Insert a row of data
                    c.execute(db_query_string)
                    db_query_success = True
            except Exception, e:
                print "Query Execution failure"
                print e
                db_query_success = False
                
            if(db_query_success):
                # Save (commit) the changes
                print "Saving changes to database"
                conn.commit()
                        
        
    except Exception, e:
        #cleanup to prevent database not accessible later
        print "General database failure , now cleanup"
        print e
        conn.close()
        conn_closed = True
    
    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    if(not conn_closed):
        print "Closing connection"
        conn.close()
###### End of Main function ########################