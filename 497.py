# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:11:02 2018

@author: nkkou
"""
from urllib.request import urlopen
from bs4 import BeautifulSoup

p = urlopen('https://news.psu.edu/campus/erie')
soup = BeautifulSoup(p,"lxml")
soup.prettify
for row in soup.find_all('h2',attrs={"class" : "node-title"}):
    print(row.text)