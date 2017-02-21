import pandas as pd


def load_manhattan_zips():
    df_zip = pd.read_csv('manhattan_zip_codes.tsv', sep='\t')
    return df_zip


def load_census_data():
    df_pop = pd.read_csv('census_pop.csv')
    df_pop.columns = ['Zip Code', 'Population']
    return df_pop


def load_populated_manhattan_zips():
    df_zip = load_manhattan_zips()
    df_pop = load_census_data()
    df_populated_zip = df_pop.merge(df_zip, on='Zip Code', how='inner')
    return df_populated_zip
