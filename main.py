from bs4 import BeautifulSoup as bs
import numpy as np
import requests as req
import json
from openai import OpenAI
import csv
from ukpostcodeutils import validation
from config import keyC,keyG

is_model_ass = 0
successfulruns = 0
is_GAPI_ass = 0
full_failure = 0

print("starting program")

client = OpenAI(api_key = keyC)

#&maxDaysSinceAdded=14
test_url = r"https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=POSTCODE%5E3700772&radius=10.0&channel=RENT&transactionType=LETTING&furnishTypes=furnished&minBathrooms=1&letType=longTerm&dontShow=retirement&minPrice=200&sortType=6&displayLocationIdentifier=undefined&maxPrice=3000&minBedrooms=3&index="

website = req.get(test_url)
soup = bs(website.text,'html.parser')
pages = soup.find("div", class_= 'Pagination_pageSelectContainer__zt0rg')

number = pages.find_all("span")

x = number[1].text
number_of_pages = ''
window_for_pages = []
for j in str(x):
        if j.isdigit() == True:
            window_for_pages.append(j)
        else:
            pass
for i in range(len(window_for_pages)):
    number_of_pages += str(window_for_pages[i])

number_of_pages = int(number_of_pages)
current_page_number = 0
page_check = 0
first_check = 0

property_and_properties = []
non_duration_property_and_properties = []

print("successful startup")

while page_check == 0:
    print(f"Currently on page {current_page_number + 1} out of {number_of_pages}.")
    url = test_url

    if current_page_number == number_of_pages and first_check == 0:
        url += str(0)
        page_check = 1
    else:
        url += str(current_page_number*24)

    website = req.get(url)

    soup = bs(website.text,'html.parser')

    propertylist = soup.find_all("address",class_="PropertyAddress_address__LYRPq")
    type_list = soup.find_all("div", class_="PropertyInformation_container__2wY0G")
    bath_list = soup.find_all("div", class_="PropertyInformation_bathContainer__ut8VY")
    descript_list = soup.find_all("p", class_="PropertyCardSummary_summary__oIv57")
    price_list = soup.find_all("div", class_="PropertyPrice_price__VL65t")
    estate_list = soup.find_all("span", class_="MarketedBy_joinedText__HTONp")
    link_list_soup = soup.find_all("a", class_="propertyCard-link")

    link_list = []
    for i in link_list_soup:
        link_list.append("rightmove.co.uk" + str(i.get("href")))

    name_list = []
    for i in estate_list:
        check = 0
        name = ''
        skip = 0
        x = str(i.string)
        for j in range(len(x)):
            if skip == 1:
                pass
            elif x[j] == ' ' and x[j-2] + x[j-1] == 'by':
                check = 1
            elif x[j] == ',' and name != '':
                skip = 1
            elif check == 1:
                name += x[j]
            else:
                pass
        name_list.append(str(name))
    
    true_price_list = []
    for i in price_list:
        check = 0
        name = ''
        skip = 0
        x = str(i.string)
        for j in x:
            try:
                int(j)
                name += str(j)
            except:
                pass
        true_price_list.append(int(name))



    for i in range(len(propertylist)):
        failed_cycle = 0
        print(f"processing {i+1} listing out of {len(propertylist)} on this page")
        if "OpenRent" in name_list[i]:
            successfulruns +=1
            print("I HATE OPENRENT")
            continue
        # elif true_price_list[i]>3200:
        #     successfulruns += 1
        #     print("Outside range.")
        #     continue
        else:
            pass
        window = []
        window.append(propertylist[i].string)
        window.append(type_list[i].find("span").string)
        window.append(bath_list[i].find("span").string + ' bathrooms')
        window.append(descript_list[i].string)
        window.append(price_list[i].string)
        window.append(name_list[i])

        print("sending to gpt-mini")

        response = client.responses.create(
            model="gpt-4o-mini-2024-07-18",
            input=[
                {
                    "role" : "developer",
                    "content" : "Guess the location based on the data, and return a full approximate postcode only, with nothing else within the response."
                }, 
                {
                    "role" : "user",
                    "content" : str(window)
                }
            ]
        )

        postcode = response.output_text
        if validation.is_valid_postcode(''.join(str(postcode).split())) == True:
            pass
        else:
            is_model_ass += 1
            print("resending to gpt4.1")
            response = client.responses.create(
            model="gpt-4.1-2025-04-14",
            input=[
                {
                    "role" : "developer",
                    "content" : "Guess the location based on the data, and return a full approximate postcode only, with nothing else within the response. You must return a full postcode."
                }, 
                {
                    "role" : "user",
                    "content" : str(window)
                }
            ]
            )

            postcode = response.output_text
            if validation.is_valid_postcode(''.join(str(postcode).split())) == True:
                pass
            else:
                raise Exception("ChatGPT Unable to find Postcode for: " + str(window))
        

        print("sending to GAPI")
        duration = 0

        headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': keyG,
            'X-Goog-FieldMask': 'routes.duration',
        }
        json_data = {
            'origin': {
                'address' : str(postcode)
            },
            'destination': {
                'address' : "SW7 2AZ"
            },
            'travelMode': 'Transit',
            'regionCode' : 'uk',
            'computeAlternativeRoutes': False,
            'languageCode': 'en-UK',
            'units': 'METRIC',
        }

        api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
        json_data = api_data.text

        data = json.loads(json_data)
        try:
            duration_1 = int(str(data['routes'][0]['duration'])[:-1:])
        except:
            try:
                print("changing postcode to latlong")
                is_GAPI_ass += 1
                website = req.get("https://findthatpostcode.uk/postcodes/" + postcode)
                data = json.loads(website.text)
                latlong = data["data"]["attributes"]["location"]
                headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': keyG,
                'X-Goog-FieldMask': 'routes.duration',
                }
                json_data = {
                'origin': {
                    "location" :{
                    "latLng" : {
                    "latitude" : latlong["lat"],
                    "longitude" : latlong["lon"]
                }
                } 
                },
                'destination': {
                    'address' : "SW7 2AZ"
                },
                'travelMode': 'Transit',
                'regionCode' : 'uk',
                'computeAlternativeRoutes': False,
                'languageCode': 'en-UK',
                'units': 'METRIC',
                }
                api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
                json_data = api_data.text
                data = json.loads(json_data)
                duration_1 = int(str(data['routes'][0]['duration'])[:-1:])
            except:
                print("Unable to process")
                full_failure +=1
                failed_cycle = 1
        if failed_cycle == 1:
            continue
        headers = {
                'Content-Type': 'application/json',
                'X-Goog-Api-Key': keyG,
                'X-Goog-FieldMask': 'routes.duration',
            }

        json_data = {
                'origin': {
                    'address' : str(postcode)
                },
                'destination': {
                    'address' : "SW7 2AZ"
                },
                'travelMode': 'Walk',
                'regionCode' : 'uk',
                'computeAlternativeRoutes': False,
                'languageCode': 'en-UK',
                'units': 'METRIC',
            }

        api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
        json_data = api_data.text

        data = json.loads(json_data)

        try:
            duration_2 = int(str(data['routes'][0]['duration'])[:-1:])
        except:
            website = req.get("https://findthatpostcode.uk/postcodes/" + postcode)
            data = json.loads(website.text)
            latlong = data["data"]["attributes"]["location"]
            headers = {
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': keyG,
            'X-Goog-FieldMask': 'routes.duration',
            }
            json_data = {
            'origin': {
                "location" :{
                "latLng" : {
                "latitude" : latlong["lat"],
                "longitude" : latlong["lon"]
            }
            } 
            },
            'destination': {
                'address' : "SW7 2AZ"
            },
            'travelMode': 'Walk',
            'regionCode' : 'uk',
            'computeAlternativeRoutes': False,
            'languageCode': 'en-UK',
            'units': 'METRIC',
            }
            api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
            json_data = api_data.text
            data = json.loads(json_data)
            duration_2 = int(str(data['routes'][0]['duration'])[:-1:])

        window.append(link_list[i])

        if duration_2 < duration_1:
            window.append("Walk")
            duration = duration_2
        else:
            window.append("Transit")
            duration = duration_1
        window.append(duration)
        property_and_properties.append(window)
        successfulruns +=1


    first_check = 1
    current_page_number += 1
    if current_page_number == number_of_pages and first_check == 1:
        page_check = 1
    print(f"Mini has failed me {is_model_ass} times out of {successfulruns}. GAPI has failed me {is_GAPI_ass} times as well. We have had {full_failure} total failures.") 

prop_name_list = []
duration_list = []
for i in range(len(property_and_properties)):
    prop_name_list.append(property_and_properties[i][0])
    duration_list.append(property_and_properties[i][-1])

filtered_prop_list = []

for i in range(len(duration_list)):
    if duration_list[i] < 45*60:
        filtered_prop_list.append(property_and_properties[i])

sorted_list = sorted(filtered_prop_list, key = lambda x : x[-1])

second_list = []
for i in sorted_list:
    window = []
    window.append(i[0])
    window.append(i[4])
    window.append(i[-1])
    window.append(i[-2])
    window.append(i[-3])
    second_list.append(window)

fields = ["Name","Price per Month","Commute Length","Commute Type", "Link"]
with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\data.csv',"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(second_list)


