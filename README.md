# NYC Grocery Store Analysis using Pymc
See blog post at making.dia.com for background/explanation

## Introduction
Does the spatial distribution of grocery stores in Manhattan reflect the spatial distribution of Manhattan's population? If not, why not?

## Data

The [Yelp API](https://github.com/Yelp/yelp-fusion) was used to collect data on locations of grocery stores in Manhattan. See `yelp_fusion_api.py` and `trawl_yelp.py`. The final results are collected in ``df_yelp_cleaned_up.csv``. Census data was used as features for the regression (at the zip code level). See ``census_data.csv`` (obtained from here: http://www.psc.isr.umich.edu/dis/census/Features/tract2zip/). Finally, the analysis was restricted to Manhattan by using a manually created list of Manhattan zip codes. See ``manhattan_zip_codes.tsv``. All of this ignores the somewhat subtle distinction between zip codes and ZCTAs (see here: https://www.census.gov/geo/reference/zctas.html).

## Modeling

A Poisson regression was implemented using pymc3. The analysis can be found in the jupyter notebook ``Model.ipynb``.

## Visualization

Shape files for zip codes from the census (https://www.census.gov/geo/maps-data/data/cbf/cbf_zcta.html) were used to plot the results on a zip code level. (For more detail, please see the blog post.) I have not included these in the repository, but they are easy enough to download.


