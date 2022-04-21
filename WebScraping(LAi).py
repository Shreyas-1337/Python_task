import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import re
import string
import json

url = 'https://github.com/scikit-learn/scikit-learn/blob/0fb307bf3/sklearn/ensemble/_forest.py#L884'

resp = uReq(url)
Data = resp.read()
resp.close()

page_soup = soup(Data, 'html.parser')
table_data = page_soup.findAll("table",{"class":"highlight tab-size js-file-line-container"})
t_d = table_data[0]
container = t_d.findAll("td",{"class":"blob-code blob-code-inner js-file-line"})

"""Extracting data of just one Class"""
data = []
for i in range(len(container)):
    data.append(container[i].span.text)    
while("" in data):
    data.remove("")

"""To find the exact loction of Start and End points"""

start = 0
end = 0
for i in range(len(data)):
    if data[i] == '    Parameters':
        start = i + 2
    if data[i] == '    Attributes':
        end = i - 1
    if data[i] == '    Notes':
        N_start = i + 2

"""Extract the Descriptions"""

def Description(start, end):
    text = ""
    for i in range(start,end):
        
        text = text + ' ' + data[i].strip()
    return text

"""Extract name and default value of parameter"""

P_Name = []
P_Value = []
strt = []
def Parameters(start, end):
    parameters = []
    for i in range(start,end):
        if (len(data[i]) - len((data[i]).lstrip(' '))) == 4:
            if (len(data[i+1]) - len((data[i+1]).lstrip(' '))) > 8:
                String = data[i] + data[i+1]
                x = i + 2
                strt.append(x)
            elif (len(data[i+1]) - len((data[i+1]).lstrip(' '))) == 8:
                String = data[i]
                x = i + 1
                strt.append(x)
            parameters = Parameter(String)
            P_Name.append(parameters[0])
            P_Value.append(parameters[1])
    x = end + 1
    strt.append(x)

def Parameter(Text):
    text = Text.split()
    name = text[0]
    word= text[-1].split("=",1)
    value = word[-1]
    return name, value

description = Description(0, (start-2))

Parameters(start, end)
P_Description = []
for i in range(len(strt)-1):
    Text = Description((strt[i]), ((strt[i+1]) - 1))
    P_Description.append(Text)

N_Description = Description(N_start, (len(data)))

#Creating Dictionary of Parameters

P = {}
for i in range (1,len(P_Name)):
    P["Parameter{0}".format(i)] = {}
    P["Parameter{0}".format(i)]["Name"] = P_Name[i]
    P["Parameter{0}".format(i)]["Default_Value"] = P_Value[i]
    P["Parameter{0}".format(i)]["Description"] = P_Description[i]

#Converting Dictionary to Json object
Json_object = json.dumps(Dictionary)

print(Json_object)