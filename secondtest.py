# import requests as req
# from bs4 import BeautifulSoup as bs
# import csv
# import json
# from config import keyG
# # test_url = r"https://www.rightmove.co.uk/property-to-rent/find.html?searchLocation=W2&useLocationIdentifier=true&locationIdentifier=OUTCODE%5E2762&radius=5.0&letType=longTerm&minBedrooms=5&maxBedrooms=5"

# # website = req.get(str(test_url))
# # soup = bs(test_url,'html.parser')
# # print(soup)
# # # pages = soup.find("div", class_= 'Pagination_pageSelectContainer__zt0rg')

# # # number = pages.find_all("span")

# # import numpy as np

# # problem = [['a','b',5],['e','f',6],['c','d',20]]

# # list_ = []

# # sorted_list = sorted(problem, key = lambda x : x[-1])

# # print(sorted_list)

# # second_list = []
# # for i in sorted_list:
# #     second_list.append(i[-2])

# # with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\data.csv',"w",newline='') as f:
# #     writer = csv.writer(f)
# #     writer.writerows(second_list)

# # from ukpostcodeutils import validation

# # postcode = "The postcode is SW13 9JT"

# # if validation.is_valid_postcode(''.join(str(postcode).split())) == True:
# #     print("Works")
# # else:
# #     print("Does not")

# # import pgeocode

# postcode = "SW13 9JT"
# # place = pgeocode.Nominatim('gb')
# # x = place.query_postal_code(postcode)
# # print(x)


# headers = {
#     'Content-Type': 'application/json',
#     'X-Goog-Api-Key': keyG,
#     'X-Goog-FieldMask': 'routes.duration',
# }
# json_data = {
#     'origin': {
#         'address' : postcode
#     },
#     'destination': {
#         'address' : "SW7 2AZ"
#     },
#     'travelMode': 'Transit',
#     'regionCode' : 'uk',
#     'computeAlternativeRoutes': False,
#     'languageCode': 'en-UK',
#     'units': 'METRIC',
# }

# api_data_2 = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
# json_data_2 = api_data_2.text

# data_2 = json.loads(json_data_2)

# print(data_2)

# website = req.get("https://findthatpostcode.uk/postcodes/" + postcode)

# data = json.loads(website.text)

# latlong = data["data"]["attributes"]["location"]

# headers = {
#             'Content-Type': 'application/json',
#             'X-Goog-Api-Key': keyG,
#             'X-Goog-FieldMask': 'routes.duration',
#         }
# json_data = {
#     'origin': {
#         "location" :{
#             "latLng" : {
#                 "latitude" : latlong["lat"],
#                 "longitude" : latlong["lon"]
#             }
#         } 

#     },
#     'destination': {
#         'address' : "SW7 2AZ"
#     },
#     'travelMode': 'Transit',
#     'regionCode' : 'uk',
#     'computeAlternativeRoutes': False,
#     'languageCode': 'en-UK',
#     'units': 'METRIC',
# }

# api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
# json_data = api_data.text

# data = json.loads(json_data)
# print(data)


try:
    int("hey")
except:
    try:
        print("hey")
    except:
        pass


