import requests as req
from bs4 import BeautifulSoup as bs
import numpy as np
import json
import csv
from config import keyG

user_duration = 41 * 60 # max transit length in seconds
user_walk_duration = 16 * 60

skip_GAPI = 0

unsort_list = []
def inputcontroller(minbed, maxbed, maxprice, minbath,maxbath,minprice = "default"):
    base_url = r"https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=POSTCODE%5E3700772&radius=20.0&channel=RENT&transactionType=LETTING&furnishTypes=furnished&sortType=6&letType=longTerm&dontShow=retirement"
    if minbed != 0:
        base_url += "&minBedrooms="+ str(minbed)
    if maxbed != 0:
        base_url += "&maxBedrooms="+ str(maxbed)
    if maxprice != 0:
        base_url += "&maxPrice="+ str(maxprice)
    if minbath != 0:
        base_url += "&minBathrooms="+ str(minbath)
    if maxbath != 0:
        base_url += "&maxBathrooms="+ str(maxbath)
    if minprice != "default":
        base_url += "&minPrice=" + str(minprice)
    else:
        base_url += "&minPrice=200"

    base_url += "&index="

    return base_url

current_input = [3,0,3000,1,0]

url = inputcontroller(*current_input)

website = req.get(url)
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

while page_check == 0:
    print(f"Currently on page {current_page_number + 1} out of {number_of_pages}.")
    page_url = url

    if current_page_number == number_of_pages and first_check == 0:
        page_url += str(0)
        page_check = 1
    else:
        page_url += str(current_page_number*24)

    website = req.get(page_url)

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
        print(f"processing {i+1} listing out of {len(propertylist)} on this page")
        
        headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': keyG,
        'X-Goog-FieldMask': 'routes.duration,routes.legs.steps.travelMode,routes.legs.steps.staticDuration',
        }
        json_data = {
        'origin': {
        'address' : str(propertylist[i])
        },
            'destination': {
            'address' : "SW7 2AZ"
        },
            'travelMode': 'Transit',
            "departureTime" : "2025-09-30T08:00:00Z",
            'regionCode' : 'uk',
            'transitPreferences': {
                "allowedTravelModes" : ["RAIL","SUBWAY","TRAIN","LIGHT_RAIL"]
            },
            'computeAlternativeRoutes': False,
            'languageCode': 'en-UK',
            'units': 'METRIC',
        }

        api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
        json_data = api_data.text
        data = json.loads(json_data)

        try:
            duration = int(str(data['routes'][0]['duration'])[:-1:])
            throwaway = data['routes'][0]['legs'][0]['steps']
        except:
            print("Skipped due to incorrect formatting")
            skip_GAPI += 1
            continue

        first_walk_duration = 0
        for j in data['routes'][0]['legs'][0]['steps']:
            if j['travelMode'] == 'WALK':
                new = ''
                for x in j['staticDuration']:
                    try:
                        int(x)
                        new += str(x)
                    except:
                        break
                first_walk_duration += int(new)
            elif j['travelMode'] == 'TRANSIT':
                break
        
        


        if duration > user_duration or first_walk_duration > user_walk_duration:
            continue
    
        window = []
        window.append(propertylist[i].string)
        # window.append(type_list[i].find("span").string)
        # window.append(bath_list[i].find("span").string + ' bathrooms')
        # window.append(descript_list[i].string)
        window.append(price_list[i].string)
        # window.append(name_list[i])
        window.append(first_walk_duration)
        window.append(duration)
        window.append(link_list[i])

        
        unsort_list.append(window)
    
    first_check = 1
    current_page_number += 1
    if current_page_number == number_of_pages and first_check == 1:
        page_check = 1


second_list = []
for i in unsort_list:
    window = []
    window.append(i[0]) # address
    window.append(i[1]) # price
    window.append(i[-3]) # walk duration
    window.append(i[-2]) # total duration
    window.append(i[-1]) # link
    second_list.append(window)

fields = ["Name","Price per Month","Walk Duration","Total Duration","Link"]
with open(r'C:\Users\Jonathan\Downloads\Web Scraper Website Files\data2.csv',"w",newline='') as f:
    writer = csv.writer(f)
    writer.writerow(fields)
    writer.writerows(second_list)

print(f"GAPI has not worked {skip_GAPI} times.")

    