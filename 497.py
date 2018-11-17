# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:11:02 2018

@author: nkkou
"""
#imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

#declarations
url = 'https://news.psu.edu/campus/erie'
titles = []
generated = []
responses = ["was Great!", "was amzaing", "was fun", "had a great vibe", "was a vibe", "meh",
             "needed more music to be fun but was alright", "needed more music", "didnt have enough to do",
             "didnt have enought people there", "was awful", "sucked", "wasn't fun"]

#Grab titles and store in array
p = urlopen(url)
soup = BeautifulSoup(p,"lxml")
soup.prettify
for row in soup.find_all('h2',attrs={"class" : "node-title"}):
    print(row.text)
    titles.append(row.text)
for i in range(len(titles)):
    x = random.randint(1,20)
    for j in range(0,x):
        r = random.randint(0,len(responses)-1)
        print(r)
        g = 'I thought ' + titles[i] + ' ' + responses[r]
        generated.append(g)
file = open("testdata.txt", "w")
for i in range(len(generated)):
    file.write(generated[i] + "\n")
file.close
    
    