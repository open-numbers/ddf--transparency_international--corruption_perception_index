# Corruption Perceptions Index

source: https://www.transparency.org/research/cpi/

no bulk download available, so we have to download data for each year.

## Notes

1. As noted in the [Release Note 2012][1], the CPI Methodology was changed in 2012 and later
and the records before 2012 were not comparable over time. 
2. The country names in source files are not consistent and contains typos, so we have to manually
map some country names to entity names in the dataset. See `country_mapping.csv` in the `etl/notebook`
folder for the mappings. 

[1]: https://www.transparency.org/files/content/pressrelease/2012_CPIUpdatedMethodology_EMBARGO_EN.pdf
