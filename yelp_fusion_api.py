"""
Code for interacting with Yelp search API.

Most is shamelessly stolen from
https://github.com/Yelp/yelp-fusion/tree/master/fusion/python
"""

import requests
import numpy as np
import config
import logging
import time
from urllib.parse import quote
from urllib.parse import urlencode


# OAuth credential placeholders that must be filled in by users.
# You can find them on
# https://www.yelp.com/developers/v3/manage_app
CONFIG = config.load_config()['yelp']
CLIENT_ID = CONFIG['CLIENT_ID']
CLIENT_SECRET = CONFIG['CLIENT_SECRET']


# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token


def request(host, path, bearer_token, url_params=None, verbose=False):
    """Given a bearer token, send a GET request to the API.

    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    if verbose:
        print('Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search_by_zipcode(bearer_token, zipcode,
                      term, page=0,
                      results_per_page=50):
    """
    Get Yelp results for a single page, searching by zipcode.

    zipcode is either a string or an integer
    """
    url_params = {
        'term': term,
        'location': str(zipcode),
        'limit': results_per_page,
        'offset': page * results_per_page
    }
    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def emit_all_by_zipcode(bearer_token, zipcode,
                        term, max_results=200,
                        results_per_page=50, delay=1):
    """Generator for all Yelp results for a search (up to max_results)."""
    pages = int(np.ceil(max_results / results_per_page))
    for page in range(pages):
        res = search_by_zipcode(bearer_token, zipcode, term,
                                page, results_per_page)
        time.sleep(delay)  # let's keep Yelp happy
        yield res


def emit_all(bearer_token, zipcodes,
             term, max_results=200,
             results_per_page=50, delay=1):
    """Generator for all Yelp results for a search in all zipcodes."""
    for zipcode in zipcodes:
        logging.info('Processing info for zip code {}'.format(zipcode))
        yield from emit_all_by_zipcode(bearer_token, zipcode, term,
                                       max_results, results_per_page, delay)
