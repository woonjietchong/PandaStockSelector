#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

import Tkinter

import sys
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice, TagExtractor
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.cmapdb import CMapDB
from pdfminer.layout import LAParams

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
        # Open a PDF file.
        #fp = open('securities_equities_300418.pdf', 'rb')
            
        # debug option
        debug = 0
        # input option
        password = ''
        pagenos = set()
        maxpages = 0
        # output option
        outfile = 'C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\extracted_output.txt'
        outtype = None
        imagewriter = None
        rotation = 0
        layoutmode = 'normal'
        codec = 'utf-8'
        scale = 1
        caching = True
        laparams = LAParams()
        
        pageiterator = 1
        
        #
        PDFDocument.debug = debug
        PDFParser.debug = debug
        CMapDB.debug = debug
        PDFResourceManager.debug = debug
        PDFPageInterpreter.debug = debug
        PDFDevice.debug = debug
        #
        rsrcmgr = PDFResourceManager(caching=caching)
        if not outtype:
            outtype = 'text'
            if outfile:
                if outfile.endswith('.htm') or outfile.endswith('.html'):
                    outtype = 'html'
                elif outfile.endswith('.xml'):
                    outtype = 'xml'
                elif outfile.endswith('.tag'):
                    outtype = 'tag'
        if outfile:
            outfp = file(outfile, 'w')
        else:
            outfp = sys.stdout
        if outtype == 'text':
            device = TextConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                   imagewriter=imagewriter)
        elif outtype == 'xml':
            device = XMLConverter(rsrcmgr, outfp, codec=codec, laparams=laparams,
                                  imagewriter=imagewriter)
        elif outtype == 'html':
            device = HTMLConverter(rsrcmgr, outfp, codec=codec, scale=scale,
                                   layoutmode=layoutmode, laparams=laparams,
                                   imagewriter=imagewriter)
        elif outtype == 'tag':
            device = TagExtractor(rsrcmgr, outfp, codec=codec)
        else:
            return 0

        fp = file('securities_equities_300418.pdf', 'rb')
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        print("----- start intepreting -------")
        for page in PDFPage.get_pages(fp, pagenos,
                                      maxpages=maxpages, password=password,
                                      caching=caching, check_extractable=True):
            print("==== page ====="+str(pageiterator))
            page.rotate = (page.rotate+rotation) % 360
            interpreter.process_page(page)
            pageiterator = pageiterator + 1
            print("=== end of page ====="+str(pageiterator))
        print("----- end of intepreting -------")
        fp.close()
        device.close()
        outfp.close()
            
        
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
