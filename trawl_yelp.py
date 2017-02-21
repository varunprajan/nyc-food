"""Trawl through zipcodes and return business attributes using Yelp API."""

import yelp_fusion_api as yfa
import dataset_loader as dl
import pandas as pd


def emit_business_data(json):
    """Generator for businesses from a single Yelp json."""
    for business_dict in json['businesses']:
        loc = business_dict['location']
        address = ', '.join(loc['display_address'])
        zipcode = int(loc['zip_code'])
        name = business_dict['name']
        coords = business_dict['coordinates']
        lat, lon = coords['latitude'], coords['longitude']
        cats = business_dict['categories']
        categories = set(cat['alias'] for cat in cats)
        yield {'Address': address,
               'Name': name,
               'Zip Code': zipcode,
               'Categories': categories,
               'Latitude': lat,
               'Longitude': lon}


def emit_all_yelp_fields(bearer_token, zipcodes,
                         term='Grocery', max_results=150):
    """Generator for businesses from Yelp jsons for all zipcodes."""
    for json in yfa.emit_all(bearer_token, zipcodes,
                             term=term, max_results=max_results):
        yield from emit_business_data(json)


def cleanup(df_yelp):
    """
    Cleanup dataframe to get high-quality data.

    Specifically:
    1) eliminate duplicates (there are a lot of these, because
    we're searching by zipcode)

    2) eliminate non-grocery stores (depending on how many results are
    returned, there may be many of these)

    3) eliminate stores with no zip code (these correspond to food trucks
    and the like)

    4) eliminate stores with zip codes outside of Manhattan (occasionally
    returned results may be for the Bronx, Jersey, etc.)
    """
    df = df_yelp.copy()
    # eliminate duplicates, assume addresses are unique
    df = df.drop_duplicates(subset='Address')

    # eliminate non-groceries
    good_idx = df['Categories'].apply(lambda x: 'grocery' in x)
    df = df[good_idx]

    # eliminate stores with no zipcode
    bad_idx = (df['Zip Code'] == '') | df['Zip Code'].isnull()
    df = df[~bad_idx]

    # eliminate zip codes outside of manhattan
    df_zip = dl.load_manhattan_zips()
    df = df.merge(df_zip, how='inner', on='Zip Code')
    return df


def main():
    """Trawl through manhattan zip codes and dump yelp results to dataframe."""
    bearer_token = yfa.obtain_bearer_token(yfa.API_HOST, yfa.TOKEN_PATH)
    df_populated_zip = dl.load_populated_manhattan_zips()
    zipcodes = df_populated_zip['Zip Code']
    df_yelp = pd.DataFrame(emit_all_yelp_fields(bearer_token, zipcodes))
    df_yelp.to_csv('df_yelp_pre_cleanup.csv')
    df_yelp = cleanup(df_yelp)
    df_yelp.to_csv('df_yelp_final.csv')


if __name__ == '__main__':
    main()
