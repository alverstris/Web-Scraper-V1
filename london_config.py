from bs4 import BeautifulSoup as bs
import numpy as np
import requests as req
import json


# start with location data

start_url = r'https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=OUTCODE%5E'

file = open(r"C:\Users\Jonathan\Downloads\Web Scraper Website Files\PostToOut.txt")

PostcodeToOutcode_dict = json.load(file)

keys = PostcodeToOutcode_dict.keys()

london_dict = {}
for i in keys:
    x = ''
    for j in i:
        try:
            int(j)
        except:
            x += j
    if x == 'E' or x == 'EC' or x == 'N' or x =='NW' or x == 'SE' or x == 'SW' or x == 'W' or x == 'WC':
        london_dict[i] = PostcodeToOutcode_dict[i]
    else:
        continue

# print(london_dict['E2'])

with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\London_Dictionary.json','w') as file:
     json.dump(london_dict,file)
