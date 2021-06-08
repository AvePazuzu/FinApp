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
import os


# =============================================================================
# finanznachrichten.de
# =============================================================================

# time of request
now = dt.datetime.now()
now_string1 = now.strftime("%d.%m.%Y %H:%M:%S")
now_string2 = now.strftime("%Y%m%d")

# kewords to itereate for search
keywords = ['hydrogen', 'nel+asa']


def latest(path):
    # get latest file in dir
    files = os.listdir(path)
    paths = [os.path.join(path, basename) for basename in files]
    return max(paths, key=os.path.getctime)


for i in range(len(keywords)):
    # define url
    url = 'https://www.finanznachrichten.de/suche/uebersicht.htm?suche='
    fin_url = url + keywords[i]
    
    # load csv today's data
    today = 'finanznachrichten/' + keywords[i] + "/" + keywords[i] + "_" + now_string2 + '.csv'
    path = 'finanznachrichten/' + keywords[i]
    try:
        data = pd.read_csv(today, sep = ';', ).drop(columns=["id"])
        # flag if new file is created
        new_file = 0
        
    except FileNotFoundError:
        # if there is no file with a date of today, latest file is loaded for comparisonof of double entries
        print('Creating new database file...')
        cols = ['Headline', 'Datetime']
        data = pd.DataFrame(columns=cols)
        data0 = pd.read_csv(latest(path), sep = ';').drop(columns=["id"])
        new_file = 1
    
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
        if new_file == 0:
            if i not in data['Headline'].tolist():
                news.append(i)
        else:
            if i not in data0['Headline'].tolist():
                news.append(i)
    
    
    # combine and export data
    cols = ['Headline']
    df = pd.DataFrame(news, columns=['Headline'])
    df['Datetime'] = now_string1
            
    data = pd.concat([df, data]).reset_index().drop(columns=["index"]).reset_index().rename(columns={'index': "id"})
    
    data.to_csv(today, sep = ';', index = False)
