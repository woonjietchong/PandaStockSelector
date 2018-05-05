#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter
from tika import parser
import re
import sqlite3
import csv

#----- Globals variables ----------
stock_symbols = []
stock_symbol_reader = None
conn_closed = False

class simpleapp_tk(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(column=0,row=0,sticky='EW')
        self.entry.bind("<Return>", self.OnPressEnter)
        self.entryVariable.set(u"Enter text here.")

        button = Tkinter.Button(self,text=u"Click me !",
                                command=self.OnButtonClick)
        button.grid(column=1,row=0)

        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,
                              anchor="w",fg="white",bg="blue")
        label.grid(column=0,row=1,columnspan=2,sticky='EW')
        self.labelVariable.set(u"Hello !")

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())       
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnButtonClick(self):
        parsedPDF = parser.from_file("C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\securities_equities_300418.pdf")
        parsedContent = parsedPDF["content"]
        
        # remove ','
        translation = {44: None}
        parsedContent = parsedContent.translate(translation)

        outputfile = open('C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\extracted_output.txt','w')
        outputfile.write(parsedContent)
        outputfile.close() 

        regexMatches = re.findall(r"([0-9][0-9])/([0-9][0-9])/([0-9][0-9][0-9][0-9]) ([0-9][0-9][0-9][0-9][A-Z0-9]??[A-Z0-9]??) (.*) MYR (.*) (.*) (.*) (.*) (.*) (.*)", parsedContent)#, re.MULTILINE)
        #regexMatches = re.match(r"([0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9]) ([0-9][0-9][0-9][0-9][A-Z0-9]??[A-Z0-9]??) (.*) MYR (.*) (.*) (.*) (.*) (.*) (.*)", parsedContent)
        print("regexMatches.groups()")        
        for groupsInRegex in regexMatches:            
            print("----------")
            print(groupsInRegex[0])
            print(groupsInRegex[1])
            print(groupsInRegex[2])
            print(groupsInRegex[3])
            print(groupsInRegex[4])
            print(groupsInRegex[5])
            print(groupsInRegex[6])
            print(groupsInRegex[7])
            print(groupsInRegex[8])
            print(groupsInRegex[9])
            print(groupsInRegex[10])
            print("----------")
            
#        print "Starting wj stock db input"
#        conn = sqlite3.connect('klse_from_bursa.db')
#        print "after conn connect"
#        try:
#            c = conn.cursor()
#            print "after conn.cursor"
#    
#            # Create table
#            # Database Schema
#            #   symbol	            TEXT
#            #   name                TEXT
#            #   date-YYYY	        INTEGER
#            #   date-MM             INTEGER
#            #   date-DD             INTEGER
#            #   open_price          NUMERIC -> decimal 3, 2
#            #   high_price          NUMERIC -> decimal 3, 2
#            #   low_price	        NUMERIC -> decimal 3, 2
#            #   close_price	        NUMERIC -> decimal 3, 2
#            #   volume	            INTEGER -> unsigned bigInt
#            #   value_traded	      INTEGER -> unsigned bigInt
#            
#            #c.execute('''CREATE TABLE IF NOT EXISTS stocks (symbol text, date text, price real)''')
#            c.execute('''CREATE TABLE IF NOT EXISTS stocks (symbol text, name text, date_YYYY integer, date_MM integer, date_DD integer, open_price numeric, high_price numeric, low_price numeric, close_price numeric, volume integer, value_traded integer)''')
#            print "after CREATE TABLE"
#            
#            print "getting finance data from yahoo"
#            for groupsInRegex in regexMatches:            
#                print("----------")
#                current_stock_symbol = iterated_symbol
#                current_stock_name = current_stock.get_name()               #TEXT
#                
#                temp_trade_datetime = current_stock.get_trade_datetime()	#TEXT
#                  # for future reference : example of get_trade_datetime() are 2017-06-23 20:17:00 UTC+0000
#                current_stock_date_YYYY	= temp_trade_datetime[0:4]        #INTEGER
#                current_stock_date_MM = temp_trade_datetime[5:7]            #INTEGER
#                current_stock_date_DD = temp_trade_datetime[8:10]            #INTEGER
#                
#                current_stock_open_price = current_stock.get_open()         #NUMERIC -> decimal 3, 2
#                print "after get_open"
#                current_stock_high_price = current_stock.get_days_high()         #NUMERIC -> decimal 3, 2
#                print "after get_days_high"
#                current_stock_low_price	= current_stock.get_days_low()        #NUMERIC -> decimal 3, 2
#                print "after get_days_low"
#                current_stock_close_price = current_stock.get_price()	        #NUMERIC -> decimal 3, 2
#                print "after get_price"
#                current_stock_volume = current_stock.get_volume()	            #INTEGER -> unsigned bigInt
#                print "after get_volume"
#                current_stock_value_traded = current_stock.get_value_traded()	            #INTEGER -> unsigned bigInt
#                print "after get_volume"
#                
#                #First
#                db_query_string = "INSERT INTO stocks VALUES (" + "'" + current_stock_symbol + "'" 
#                print "after first"
#                db_query_string = db_query_string + ", " + "'" + current_stock_name + "'"
#                db_query_string = db_query_string + ", " + current_stock_date_YYYY
#                db_query_string = db_query_string + ", " + current_stock_date_MM
#                db_query_string = db_query_string + ", " + current_stock_date_DD                   
#                db_query_string = db_query_string + ", " + current_stock_open_price
#                db_query_string = db_query_string + ", " + current_stock_high_price
#                db_query_string = db_query_string + ", " + current_stock_low_price
#                db_query_string = db_query_string + ", " + current_stock_close_price
#                db_query_string = db_query_string + ", " + current_stock_volume
#                db_query_string = db_query_string + ", " + current_stock_value_traded
#
#                #Last                
#                db_query_string = db_query_string +")"
#    
#                print db_query_string
#                
#            try:
#                # Insert a row of data
#                c.execute(db_query_string)
#                db_query_success = True
#            except Exception, e:
#                print "Query Execution failure"
#                print e
#                db_query_success = False
#                
#            if(db_query_success):
#                # Save (commit) the changes
#                print "Saving changes to database"
#                conn.commit()
#                            
#            
#        except Exception, e:
#            #cleanup to prevent database not accessible later
#            print "General database failure , now cleanup"
#            print e
#            conn.close()
#            conn_closed = True
#        
#        # We can also close the connection if we are done with it.
#        # Just be sure any changes have been committed or they will be lost.
#        if(not conn_closed):
#            print "Closing connection"
#            conn.close()

        self.labelVariable.set( self.entryVariable.get()+" (You clicked the button)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

    def OnPressEnter(self,event):
        self.labelVariable.set( self.entryVariable.get()+" (You pressed ENTER)" )
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = simpleapp_tk(None)
    app.title('my application')
    app.mainloop()
    
#from io import BytesIO
#from io import StringIO
#
#from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
#from pdfminer.converter import TextConverter
#from pdfminer.layout import LAParams
#from pdfminer.pdfpage import PDFPage
#
##PDFMiner boilerplate
#rsrcmgr = PDFResourceManager()
#sio = StringIO()
#codec = 'utf-8'
#laparams = LAParams()
#device = TextConverter(rsrcmgr, sio, codec=codec, laparams=laparams)
#interpreter = PDFPageInterpreter(rsrcmgr, device)
#
#fp = open('C:\Users\Ozgur\Desktop\otivit\kitaplar\pdf2\salinger.pdf', 'rb')
#for page in PDFPage.get_pages(fp):
#interpreter.process_page(page)
#fp.close()
#text = sio.getvalue()
#text=text.replace(chr(272)," ")
#print(type(text))
#f = open('C:\Users\Ozgur\Desktop\otivit\kitaplar\txt2\yes.txt','w')
#f.write(text)
#
#print("hello")
    

#regex = [0-9][0-9]/[0-9][0-9]/[0-9][0-9][0-9][0-9] [0-9][0-9][0-9][0-9][A-Z0-9]??[A-Z0-9]?? .* MYR .* .* .* .* .* .*
#
# from tika import parser
# parsedPDF = parser.from_file("C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\securities_equities_300418.pdf")
# pdf = parsedPDF["content"]
# f = open('C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\extracted_output.txt','w')
# f.write(pdf)
# f.close()
