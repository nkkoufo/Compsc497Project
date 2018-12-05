import json
import random
import numpy as np
import pandas as pd
import webbrowser, os
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from collections import namedtuple
from urllib.request import urlopen
from watson_developer_cloud import NaturalLanguageUnderstandingV1 as NLU
from watson_developer_cloud.natural_language_understanding_v1 import Features,KeywordsOptions,SentimentOptions

###############################################################################
# Classes and Setters
###############################################################################

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

###############################################################################
# Declarations
###############################################################################

baseurl = 'https://news.psu.edu'
url = 'https://news.psu.edu/campus/erie'
urlToAppend = 'https://news.psu.edu/campus/erie?type=top&page='
titles = []
generated = []
responses = ["was Great!", "was amazing", "was fun", "had a great vibe", "was a vibe", "meh",
             "needed more music to be fun but was alright", "needed more music", "didnt have enough to do",
             "didnt have enought people there", "was awful", "sucked", "wasn't fun"]
responseArray = []

###############################################################################
# Grab Titles, Create Text, and Store in Array
###############################################################################

pages = 5
#DONT TOUCH THESE
i = 0
x = 0
while i < pages:
    p = urlopen(urlToAppend + str(i))
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
    for tag in soup.find_all("div", {"class": "field-items"}):
        if(tag.text and tag.p):
            generated[x].text = (tag.text)
            x = x + 1
            count1 = count1 + 1 
        
    if count1 == count2:
        print("noice")
    else: 
        print("No Fam")
        print(count1)
        print(count2)
    i = i + 1
    
###############################################################################
# Sentiment Analysis
###############################################################################

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

###############################################################################
# HTML Generation
###############################################################################

def scoreRank(x):
    if x < 0 and x >= -1:
        return "<font color=\"#FF0000\"><b>" + str(int(round(x*-100))) + "% Negative</b></font>";
    elif x > 0 and x <= 1:
        return "<font color=\"#00FF00\"><b>" + str(int(round(x*100))) + "% Positive</b></font>";
    elif x == 0:
        return "<font color=\"#000000\"><b>Neutral</b></font>";

num_positive = 0
num_negative = 0
num_neutral = 0

for item in generated:
    if item.score < 0 and item.score >= -1:
        num_negative = num_negative + 1
    elif item.score > 0 and item.score <= 1:
        num_positive = num_positive + 1
    elif item.score == 0:
        num_neutral = num_neutral + 1

pie_labels = 'Positive', 'Negative', 'Neutral'
pie_sizes = [num_positive, num_negative, num_neutral]
pie_colors = ['lightgreen', 'lightcoral', 'lightgrey']
pie_explode = (0.1, 0, 0)

plt.pie(pie_sizes, explode=pie_explode, labels=pie_labels, colors=pie_colors, 
        autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.savefig('pie.png')
plt.show()

plt.close()

hist_list_pos = []
hist_list_neg = []
hist_list_neu = []
for item in generated:
    if item.score > 0:
        hist_list_pos.append(item.score)
    elif item.score < 0:
        hist_list_neg.append(item.score)
    else:
        hist_list_neu.append(item.score)

legend = ['Positive', 'Negative', 'Neutral']

plt.hist([hist_list_pos, hist_list_neg, hist_list_neu], 
         color=['lightgreen', 'lightcoral', 'lightgrey'], bins=10)
plt.xlabel("Scores")
plt.ylabel("Frequency of Scores")
plt.title("Dispersion of Event Scores")
plt.legend(legend)
plt.xticks(np.arange(-0.5, 1, 0.5))
plt.yticks(np.arange(0, 30, 5))
plt.savefig('hist.png')
plt.show()

plt.close()

filename = 'index.html'

html_str = """
<!doctype html>
<html lang="en">
    <head> 
        <meta charset="UTF-8">
        <title>CMPSC497 | Behrend Events Sentiment Analyzer</title>
    </head>
    <style>
        table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 95%;
        }
        td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
        }
        tr:nth-child(even) {
                background-color: #dddddd;
        }
        body {
                margin:0;
        }
        .header {
                width:100%;
                padding:40px;
                font-size:3em;
                background-color:#666699;
                color:white;
                font-family:Verdana;
        }
        .table_holder {
                padding-top: 20px;
        }
        .imageclass {
                display: inline-block;
                margin-left: auto;
                margin-right: auto;
        }
        #images {
                text-align: center;
        }
    </style>
    <body>
        <div class="header">Behrend Event Sentiment Analysis</div>
        <div id="images">
            <img class="imageclass" src="pie.png" alt="Pie Chart" style="width:33%">
            <img class="imageclass" src="hist.png" alt="Histogram" style="width:33%">
        </div>
        <div class="table_holder">
            <table align="center">
                <tr>
                    <th>Headline</th>
                    <th>Score</th>
                </tr>        
"""

for item in generated:
    html_str = html_str + """
        <tr>
            <td>
                <a href="
    """ + item.link + """
                ">
    """ + item.title + """ 
                </a>
            </td>
            <td>
    """ + str(scoreRank(item.score)) + """
            </td>
        </tr>
    """

html_end_body = """     
            </table>   
        </div>
        <div class="table_holder">
        </div>
    </body>
</html>
"""

html_str = html_str + html_end_body

html_file = open(filename, "w")
html_file.write(html_str)
html_file.close()

html_url = 'file://' + os.path.realpath(filename)
webbrowser.open_new(html_url)



























