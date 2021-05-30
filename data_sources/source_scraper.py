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
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.request import Request

# =============================================================================
# 
# =============================================================================

tick = 'https://www.finanznachrichten.de/suche/uebersicht.htm?suche='

tickers = ['wasserstoff', 'hydrogen']

# Get Data
finanzn_url = tick

news_tables = {}

y_url = tick + tickers[1]
req = Request(url=y_url,headers={'user-agent': 'my-app/0.0.1'}) 
resp = urlopen(req)    
html = BeautifulSoup(resp, 'lxml')
news_table = html.find('tbody', {'class': 'table-hoverable table-alternating-rows'})
news_tables[tickers[0]] = news_table

df = news_tables[tickers[0]]
df_tr = df.findAll('a')


kk = news_table.findAll({'span', 'a'})

kk3 = {x.get_text() for x in kk}

kk4=[]
for v in kk3:

    if len(v) > 25:
        kk4.append(v)

cols = ['Head']
df = pd.DataFrame(kk4, columns=cols)