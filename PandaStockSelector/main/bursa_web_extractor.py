# -*- coding: utf-8 -*-
"""
Created on Sun May 06 08:12:41 2018

@author: Admin
"""

#import requests
import wget

###### Main function ########################
if __name__ == '__main__':
    url = 'http://www.google-analytics.com/__utm.gif?utmwv=5.7.2&utms=9&utmn=202270969&utmhn=www.bursamalaysia.com&utmt=event&utme=5(Link*clicked*%2Fmisc%2Fsystem%2Fequity_market_statistics%2Fsecurities_equities_260418.pdf)&utmcs=UTF-8&utmsr=1366x768&utmvp=771x369&utmsc=24-bit&utmul=en-us&utmje=0&utmfl=-&utmdt=Market%20Statistics%20%7C%20Bursa%20Malaysia%20Market&utmhid=359827776&utmr=0&utmp=%2Fmarket%2Fsecurities%2Fequities%2Fmarket-statistics%2F&utmht=1525567159326&utmac=UA-30320123-1&utmcc=__utma%3D133856029.1919579433.1525157637.1525157637.1525565383.2%3B%2B__utmz%3D133856029.1525157637.1.1.utmcsr%3Dgoogle%7Cutmccn%3D(organic)%7Cutmcmd%3Dorganic%7Cutmctr%3D(not%2520provided)%3B&utmjid=&utmu=6BCAAAAAAAAAAAAAAAAAAAAE~'  
    wget.download(url, '2604.pdf') 
    
#    downloadurl = 'http://www.bursamalaysia.com/misc/system/equity_market_statistics/securities_equities_020518.pdf'      
#    downloadheaders = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#
#    response = requests.get(downloadurl, headers=downloadheaders)
#    print(response.content)
#    
#    downloadedfile = open('C:\Users\Admin\Desktop\PandaStockSelectorWorkspace\PandaStockSelector\main\securities_equities_020518.txt','w')
#    downloadedfile.write(response.content)
#    downloadedfile.close() 

