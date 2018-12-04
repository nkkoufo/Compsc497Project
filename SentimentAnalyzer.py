# -*- coding: utf-8 -*-
"""
Created on Sat Nov 17 15:48:22 2018
@author: zcast7172
"""
from collections import namedtuple
import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features,KeywordsOptions,SentimentOptions
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random

#classes and setters
class generatedWebElement(object):
    text = ""
    title = ""
    link = ""
    score = 0.0
class generatedElement(object):
    text = ""
    title = ""
    
class responseArrayElement(object):
    text = ""
    score = 0.0
    title = ""

def make_gE(text, title):
    a = generatedElement()
    a.text = text
    a.title = title
    return a

def make_RAE(text, score, title):
    a = responseArrayElement()
    a.text = text
    a.score = score
    a.title = title
    return a

def make_GWE(text, title, link, score):
    a = generatedWebElement()
    a.text = text
    a.title = title
    a.link = link
    a.score = score
    return a

#declarations
baseurl = 'https://news.psu.edu'
url = 'https://news.psu.edu/campus/erie'
titles = []
generated = []
responses = ["was Great!", "was amazing", "was fun", "had a great vibe", "was a vibe", "meh",
             "needed more music to be fun but was alright", "needed more music", "didnt have enough to do",
             "didnt have enought people there", "was awful", "sucked", "wasn't fun"]
responseArray = []
"""
for row in soup.find_all('h2',attrs={"class" : "node-title"}):
    print(row.text)
    titles.append(row.text)
for i in range(len(titles)):
    x = random.randint(1,20)
    for j in range(0,x):
        r = random.randint(0,len(responses)-1)
        print(r)
        g = make_gE('I thought ' + titles[i] + ' ' + responses[r], titles[i])
        generated.append(g)
"""

#Grab titles create text and store in array
p = urlopen(url)
soup = BeautifulSoup(p,"lxml")
soup.prettify
count1 = 0
count2 = 0
for row in soup.find_all('h2', {"class" : "node-title"}):
    title = (row.text)
    link = (baseurl + row.a['href'])
    r = make_GWE("", title, link, 0.0)
    count2 = count2 + 1
    generated.append(r)
i = 0
for tag in soup.find_all("div", {"class": "field-items"}):
    if(tag.text and tag.p):
        generated[i].text = (tag.text)
        i = i + 1
        count1 = count1 + 1 
        
if count1 == count2:
    print("noice")
else: 
    print("No Fam")
    print(count1)
    print(count2)
    
    
    
    

        

    

#sentiment analysis
nlu = NLU(version='2018-03-16',
          iam_apikey='SXP-aQb8p1wxsCr3wY_9VVgoJGyXQISul6L4DjNsN4Di',
          url='https://gateway.watsonplatform.net/natural-language-understanding/api')
i = 0
for item in generated:
    response = nlu.analyze(
            text = item.text,
            return_analyzed_text=True,
            DocumentSentimentResults=True,
            features=Features(
            sentiment=SentimentOptions(document=True)
            )).get_result()
    print(json.dumps(response, indent=2))
    score = response["sentiment"]["document"]["score"]
    text = response["analyzed_text"]
    title = item.title
    generated[i].score = score
    i = i + 1
    

#generated[i].text to get the text you can also do .title, .score and .link
