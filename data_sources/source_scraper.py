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
    - load todays news store file
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
now_string1 = now.strftime("%d.%m.%Y %H:%M:%S")
now_string2 = now.strftime("%Y%m%d")

# kewords to itereate for search
keywords = ['hydrogen', 'nel+asa']

for i in range(len(keywords)):
    # define url
    url = 'https://www.finanznachrichten.de/suche/uebersicht.htm?suche='
    fin_url = url + keywords[i]
    
    # load csv
    path = 'finanznachrichten/' + keywords[i] + "/" + keywords[i] + "_" + now_string2 + '.csv'
    
    try:
        data = pd.read_csv(path, sep = ';', ).drop(columns=["id"])
        
    except FileNotFoundError:
        print('Creating new database file...')
        cols = ['Headline', 'Datetime']
        data = pd.DataFrame(columns=cols)
    
    # request url and recieve the respond   
    req = Request(url=fin_url,headers={'user-agent': 'FinApp/0.0.1'}) 
    resp = urlopen(req)    
    html = BeautifulSoup(resp, 'lxml')
    
    # find news table in the html body
    news_table = html.find('tbody', {'class': 'table-hoverable table-alternating-rows'})  
    
    # find the html lines with the news in the news table 
    html_lines = news_table.findAll({'span', 'a'})
    
    # extract the string in the html lines
    all_strings = {x.get_text() for x in html_lines}
    
    # filter for the relevant strings
    news_all=[]
    for v in all_strings:
    
        if len(v) > 25:
            news_all.append(v)
    
    
    # check for double entries and append only new head lines
    dt = data['Headline'].tolist()
    news = []
    for i in news_all:
        if i not in data['Headline'].tolist():
            news.append(i)
    
    
    # combine and export data
    cols = ['Headline']
    df = pd.DataFrame(news, columns=['Headline'])
    df['Datetime'] = now_string1
            
    data = pd.concat([df, data]).reset_index().drop(columns=["index"]).reset_index().rename(columns={'index': "id"})
    
    data.to_csv(path, sep = ';', index = False)