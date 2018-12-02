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

#declarations
url = 'https://news.psu.edu/campus/erie'
titles = []
generated = []
responses = ["was Great!", "was amazing", "was fun", "had a great vibe", "was a vibe", "meh",
             "needed more music to be fun but was alright", "needed more music", "didnt have enough to do",
             "didnt have enought people there", "was awful", "sucked", "wasn't fun"]
responseArray = []
class generatedElement(object):
    sentence = ""
    title = ""
    
class responseArrayElement(object):
    sentence = ""
    score = 0.0
    title = ""

def make_gE(sentence, title):
    a = generatedElement()
    a.sentence = sentence
    a.title = title
    return a

def make_RAE(sentence, score, title):
    a = responseArrayElement()
    a.sentence = sentence
    a.score = score
    a.title = title
    return a
    
#Grab titles create text and store in array
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
        g = make_gE('I thought ' + titles[i] + ' ' + responses[r], titles[i])
        generated.append(g)

#sentiment analysis
nlu = NLU(version='2018-03-16',
          iam_apikey='SXP-aQb8p1wxsCr3wY_9VVgoJGyXQISul6L4DjNsN4Di',
          url='https://gateway.watsonplatform.net/natural-language-understanding/api')

for item in generated:
    response = nlu.analyze(
            text = item.sentence,
            return_analyzed_text=True,
            DocumentSentimentResults=True,
            features=Features(
            sentiment=SentimentOptions(document=True)
            )).get_result()
    print(json.dumps(response, indent=2))
    score = response["sentiment"]["document"]["score"]
    text = response["analyzed_text"]
    title = item.title
    r = make_RAE(text, score, title)
    responseArray.append(r)
