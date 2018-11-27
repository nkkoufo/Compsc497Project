# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:48:22 2018

@author: zcast7172
"""
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features,KeywordsOptions
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

#declarations
url = 'https://news.psu.edu/campus/erie'
titles = []
generated = []
responses = ["was Great!", "was amazing", "was fun", "had a great vibe", "was a vibe", "meh",
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


nlu = NLU(version='2018-03-16',
          iam_apikey='SXP-aQb8p1wxsCr3wY_9VVgoJGyXQISul6L4DjNsN4Di',
          url='https://gateway.watsonplatform.net/natural-language-understanding/api')

for item in generated:
    response = nlu.analyze(
            url = 'https://news.psu.edu/campus/erie',
            features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=2))).get_result()
    print(json.dumps(response, indent=2))