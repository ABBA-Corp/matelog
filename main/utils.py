import requests
from django.conf import settings

# get city coordinates by zip
def get_coordinates(city):
    coord_params = {
        "zip": city.zip,
        "key": "17o8dysaCDrgvlc"
    }

    coord_request = requests.get(
        'https://api.promaptools.com/service/us/zip-lat-lng/get/', params=coord_params).json()
    lat = coord_request.get("output")[0].get('latitude')
    lon = coord_request.get("output")[0].get("longitude")

    return f'{lat},{lon}'


# get distance
def get_distance(ship_to, ship_from):
    point_a = get_coordinates(ship_to)
    point_b = get_coordinates(ship_from)

    distance_url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial'
    distance_params = {
        'origins': point_a,
        'destinations': point_b,
        'key': settings.GOOGLE_API_KEY
    }

    distance_request = requests.get(
        distance_url, params=distance_params).json()
    distance = distance_request.get('rows', [])[0].get('elements', [])[0].get('distance', {}).get("text")


    return distance
