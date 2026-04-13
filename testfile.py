import requests as req
from bs4 import BeautifulSoup as bs

property_and_properties = []

for z in range(11):

    test_url = r"https://www.rightmove.co.uk/property-to-rent/find.html?useLocationIdentifier=true&locationIdentifier=OUTCODE%5E2520&radius=40&channel=RENT&transactionType=LETTING.html&furnishTypes=furnished&minBathrooms=1&letType=longTerm&dontShow=retirement&minPrice=200" + r"&minBedrooms="+ str(z) + r"&maxBedrooms=" + str(z) + r"&index="

    website = req.get(test_url)
    soup = bs(website.text,'html.parser')
    pages = soup.find("div", class_= 'Pagination_pageSelectContainer__zt0rg')

    number = pages.find_all("span")

    x = number[1].text

    for j in x:
            window_for_pages = ''
            try:
                int(j)
                window_for_pages += str(j)
            except:
                pass
    number_of_pages = int(window_for_pages)

    number_of_pages -= 1
    current_page_number = 0 #inverted against real page number
    page_check = 0
    first_check = 0

    while page_check == 0:

        url = test_url
        
        if current_page_number == number_of_pages and first_check == 0:
            url += str(0)
            page_check = 1
        elif current_page_number == number_of_pages and first_check == 1:
            url += str(current_page_number * 24)
            page_check = 1
        else:
            url += str(current_page_number * 24)
        print(url)
        website = req.get(url)
        soup = bs(website.text,'html.parser')

        propertylist = soup.find_all("address",class_="PropertyAddress_address__LYRPq")
        type_list = soup.find_all("div", class_="PropertyInformation_container__2wY0G")
        bath_list = soup.find_all("div", class_="PropertyInformation_bathContainer__ut8VY")
        descript_list = soup.find_all("p", class_="PropertyCardSummary_summary__oIv57")
        price_list = soup.find_all("div", class_="PropertyPrice_price__VL65t")
        estate_list = soup.find_all("span", class_="MarketedBy_joinedText__HTONp")

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
            
        # print(name_list)

        

        for i in range(len(propertylist)):
            window = []
            window.append(propertylist[i].string)
            window.append(type_list[i].find("span").string)
            if z == 0 or 1:
                window.append("1 bedroom")
            else:
                window.append(str(z) + " bedrooms")
            window.append(bath_list[i].find("span").string + ' bathrooms')
            window.append(descript_list[i].string)
            window.append(price_list[i].string)
            window.append(name_list[i])
            property_and_properties.append(window)
        current_page_number += 1
        first_check = 1

print(property_and_properties[-1])
print(property_and_properties[1])




