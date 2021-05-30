#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 30 14:04:59 2021

@author: eugen
"""

"""
This module is developed for finding, scraping & storing news articles 
and headlines regarding financial news.

Process: 
    - find url with suitable strings
    - scrape the content via beautifullsoup
    - find and extract the required stings in the html document
    - compare if the strings are already in the database
    - write the new strings to database
"""

# Import libraries
import pandas as pd
import datetime as dt
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request


# =============================================================================
# finanznachrichten.de
# =============================================================================

# time of request
now = dt.datetime.now()
now_string = dt.strftime("%d.%m.%Y %H:%M:%S")


# define url
url = 'https://www.finanznachrichten.de/suche/uebersicht.htm?suche='

keywords = ['hydrogen']

fin_url = url + keywords[0]

# load csv




news_tables = {}

req = Request(url=fin_url,headers={'user-agent': 'FinApp/0.0.1'}) 
resp = urlopen(req)    
html = BeautifulSoup(resp, 'lxml')
news_table = html.find('tbody', {'class': 'table-hoverable table-alternating-rows'})
# news_tables[keywords[0]] = news_table


kk = news_table.findAll({'span', 'a'})

kk3 = {x.get_text() for x in kk}

kk4=[]
for v in kk3:

    if len(v) > 25:
        kk4.append(v)

cols = ['Headline']
df = pd.DataFrame(kk4, columns=cols)
df['Datetime'] = now_string

path = 'finanznachrichten/' + keywords[0]
df.to_csv(path, sep = ';', index=False)



