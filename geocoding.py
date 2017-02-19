import time
import requests
import config

GOOGLE_API_URL = """https://maps.googleapis.com/maps/api/geocode/json"""
MY_API_KEY = get_config()['api_key']


def geocoding_from_address(full_address, delay=0.05):
    if delay: # let's not anger Google
        time.sleep(delay)

    full_address = full_address.replace(' ', '+')
    url = '{}?address={}&key={}'.format(GOOGLE_API_URL,
                                        full_address,
                                        MY_API_KEY)
    geocoding_json = requests.get(url)
    return geocoding_json


def lat_long_from_geocoding(geocoding_json):

