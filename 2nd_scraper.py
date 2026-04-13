from bs4 import BeautifulSoup as bs
import numpy as np
import requests as req
import json

start_url = r'https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=OUTCODE%5E'

# we are going to check outcodes for 1 to 3000

outcode_number = np.arange(1,3000,1)

dict = {}

for i in outcode_number:
    website = req.get(str(start_url)+str(i))
    if '400' in str(website):
        continue
    soup = bs(website.text,'html.parser')
    postcode_embed = str(soup.find('h1'))[::-1]

    postcode_true = ''
    check = 0
    for j in postcode_embed:
        if j == ' ':
            break
        elif check == 1 and j != '<':
            postcode_true += str(j)
        elif j == '<':
            check = 1

    postcode_true = postcode_true[::-1]
    dict[str(postcode_true)] = str(i)

with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\PostToOut.txt','w') as file:
     json.dump(dict,file)

# test_dict = {}

# for i in outcode_number:
#     test_dict[str(i)] = str(i)

# with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\PostToOut.txt','w') as file:
#     json.dump(test_dict,file)


# test using 5E1

# test_url = r'https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=OUTCODE%5E1'

# website = req.get(str(test_url))
# soup = bs(website.text,'html.parser')
# postcode_embed = str(soup.find('h1'))[::-1]

# postcode_true = ''
# check = 0
# for i in postcode_embed:
#     if i == ' ':
#         break
#     elif check == 1 and i != '<':
#         postcode_true += str(i)
#     elif i == '<':
#         check = 1

# postcode_true = postcode_true[::-1]

# print(postcode_true)

# check how to deal with no page

# test_url = r'https://www.rightmove.co.uk/student-accommodation/find.html?locationIdentifier=OUTCODE%5E3000'

# website = req.get(str(test_url))
# soup = bs(website.text,'html.parser')

# print(website)