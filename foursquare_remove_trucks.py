#!/usr/bin/python3

import json, requests
from pymongo import MongoClient
from geopy import geocoders
import pprint

def get_foursquare():
    url = 'https://api.foursquare.com/v2/venues/explore'
    bing_key = "bNV4gwzuDF0BY7hRBr2D~SwYlwf_NvSxlbZ36oGsTdA~AthfnABkus6e2oSBb4W9Q9_7yHrFh1cHbreVFmsPad2apAgjYqLYZi8E2iSyiJk-"
    bing = geocoders.Bing(bing_key)
    params = dict(
        client_id='ODAOUA2ZUGYKSAQMGSED4HVLAGQJZF4LU1FNEESGR2KY20CL',
        client_secret='TBGFJYKBYEUHORFJH3MCBB2DKP1SFBJ4ZUK2T3TVHGKBIHYD',
        v='20171110',
        ll = '37.792085, -122.399368',
        section = 'food',
        limit = 15
)


    yelp_params = []

    r = requests.get(url=url, params=params).json()
    fs_list = (r.get('response').get('groups'))
    for post in fs_list:
        posts = (post.get('items'))
        for place in posts:
            name = (place.get('venue').get('name'))
# print(name)
            address_field = place.get('venue').get('location')
#           print(address_field)
            postal_code = address_field.get('postalCode')
            street = address_field.get('address')
            city = (address_field.get('formattedAddress')[1]).replace(",", "")[:-5]
            restaurant = {}
            price = place.get('venue').get('price')
            rating = place.get('venue').get('rating')
            reviews_count = place.get('venue').get('ratingSignals')
            restaurant['total_reviews'] = reviews_count
            standardized_rating = round((rating/10), 2)
            restaurant['standard_rating'] = standardized_rating
            rating_weight = round((reviews_count * 1.35), 2)
            restaurant['rating_weight'] = rating_weight
            try:
                address = street + " " +  city + " " + postal_code
#               print("address", address)
            except:
#               print("Removing from list\n")
                continue
            try:
                bing_location = bing.geocode(address, exactly_one=True, timeout=3)
                location = str(bing_location)
                if location is None:
                    restaurant['name'] = name
                    restaurant['location'] = address
                    yelp_params.append(restaurant)
#                       print(address)
                else:
                    restaurant['name'] = name
                    restaurant['location'] = location
                    yelp_params.append(restaurant)
#                       print(location)
#                       print("----------------------")
            except Exception as e:
                print("ERROR", e)
        return yelp_params

if __name__ == "__main__":
    get_foursquare()
