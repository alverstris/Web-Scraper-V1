import requests as req
import json

headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': 'AIzaSyD_KoGaoZA2Qrw4ljwhS8DHz3JMzusq-1I',
    'X-Goog-FieldMask': 'routes.duration',
}

json_data = {
    'origin': {
        'address' : "W2 1UF"
    },
    'destination': {
        'address' : "SW7 2AZ"
    },
    'travelMode': 'Bicycle',
    'regionCode' : 'uk',
    'computeAlternativeRoutes': False,
    'languageCode': 'en-UK',
    'units': 'METRIC',
}

api_data = req.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, json=json_data)
json_data = api_data.text

data = json.loads(json_data)
duration = str(data['routes'][0]['duration'])[:-1:]

print(str(int(duration)/60)+ ' minutes to main campus via bike.')

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{\n  "origin":{\n    "location":{\n      "latLng":{\n        "latitude": 37.419734,\n        "longitude": -122.0827784\n      }\n    }\n  },\n  "destination":{\n    "location":{\n      "latLng":{\n        "latitude": 37.417670,\n        "longitude": -122.079595\n      }\n    }\n  },\n  "travelMode": "DRIVE",\n  "routingPreference": "TRAFFIC_AWARE",\n  "computeAlternativeRoutes": false,\n  "routeModifiers": {\n    "avoidTolls": false,\n    "avoidHighways": false,\n    "avoidFerries": false\n  },\n  "languageCode": "en-US",\n  "units": "METRIC"\n}'
#response = requests.post('https://routes.googleapis.com/directions/v2:computeRoutes', headers=headers, data=data)