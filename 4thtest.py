import requests as req
import json
from config import keyG

# headers = {
#     'Content-Type': 'application/json',
#     'X-Goog-Api-Key': keyG,
#     'X-Goog-FieldMask': 'routes.duration,routes.legs.steps.travelMode,routes.legs.steps.staticDuration',
# }
# json_data = {
#     'origin': {
#     'address' : 'N1 7GU'
#     },
#         'destination': {
#         'address' : "SW7 2AZ"
#     },
#         'travelMode': 'Transit',
#         "departureTime" : "2025-09-30T08:00:00Z",
#         'regionCode' : 'uk',
#         'transitPreferences': {
#             "allowedTravelModes" : ["RAIL"]
#         },
#         'computeAlternativeRoutes': False,
#         'languageCode': 'en-UK',
#         'units': 'METRIC',
# }

# api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
# json_data = api_data.text
# data = json.loads(json_data)

# print(data['routes'][0]['legs'][0]['steps'])
# first_walk_duration = 0
# for i in data['routes'][0]['legs'][0]['steps']:
    
#     print(i)
#     if i['travelMode'] == 'WALK':
#         new = ''
#         for x in i['staticDuration']:
#             try:
#                 int(x)
#                 new += str(x)
#             except:
#                 break
#         first_walk_duration += int(new)
#     elif i['travelMode'] == 'TRANSIT':
#         break
#     print("next")

# print(data['routes'][0])

location_headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': keyG,
    'X-Goog-FieldMask': 'suggestions.placePrediction',
}
location_json_data = {
    'input': 'Stanley Gardens',
    'regionCode': 'uk',
}
location_check_api = req.post("https://places.googleapis.com/v1/places:autocomplete",headers = location_headers, json = location_json_data)

print(json.loads(location_check_api.text))