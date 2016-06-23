# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import os

from ddf_utils.str import to_concept_id
from ddf_utils.index import create_index_file


# configuration of file path
source_dir = '../source/'
out_dir = '../../'


def cleanup_data(source_dir):
    all_data = []

    for f in os.listdir(source_dir):
        if 'xls' in f:
            if '2014' in f:
                data = pd.read_excel(os.path.join(source_dir, f), skiprows=1)
                data = data[['Country / Territory', 'Unnamed: 2', 'CPI 2014 Score']]  ## unnamed 2 is wbcode
                data['year'] = 2014
                data = data.dropna()
                data.columns = ['country', 'wbcode', 'cpi', 'year']
                all_data.append(data)
            if '2015' in f:
                data = pd.read_excel(os.path.join(source_dir, f))
                data = data[['Country', 'wbcode', 'CPI2015']]
                data['year'] = 2015
                data = data.dropna()
                data.columns = ['country', 'wbcode', 'cpi', 'year']
                all_data.append(data)
            if '2010' in f:
                data = pd.read_excel(os.path.join(source_dir, f), skiprows=1)
                data = data[['Country / Territory', 'CPI 2010 Score']]
                data['year'] = 2010
                data = data.dropna()
                data.columns = ['country', 'cpi', 'year']
                all_data.append(data)
            if '2011' in f:
                data = pd.read_excel(os.path.join(source_dir, f))
                data = data[['country', 'cpi11']]
                data['year'] = 2011
                data = data.dropna()
                data.columns = ['country', 'cpi', 'year']
                all_data.append(data)
            if '2012' in f:
                data = pd.read_excel(os.path.join(source_dir, f))
                data = data[['Country / Territory', 'CPI 2012 Score']]
                data['year'] = 2012
                data = data.dropna()
                data.columns = ['country', 'cpi', 'year']
                all_data.append(data)
            if '2013' in f:
                data = pd.read_excel(os.path.join(source_dir, f))
                data = data[['Country / Territory', 'Unnamed: 2', 'CPI 2013 Score']]  ## unnamed 2 is wbcode
                data['year'] = 2013
                data = data.dropna()
                data.columns = ['country', 'wbcode', 'cpi', 'year']
                all_data.append(data)

    # concat all data and fill in wbcode column.
    all_data_df = pd.concat(all_data)
    all_data_df = all_data_df.reset_index(drop=True)
    gps = all_data_df.groupby('country')
    for k, v in gps.groups.items():
        df = all_data_df[all_data_df['country'] == k]

        wbcode_list = df['wbcode'].unique()
        wbcode_list = [x for x in wbcode_list if x is not np.nan]

        if len(wbcode_list) == 0:
            country = to_concept_id(k)

        else:
            country = wbcode_list[0]

        all_data_df.loc[v, 'wbcode'] = country

    return all_data_df


def extract_entities_country(data):
    country = data[['country', 'wbcode']].copy()
    country.columns = ['name', 'country']
    country['country'] = country['country'].map(to_concept_id)

    country = country[['country', 'name']].drop_duplicates()

    for c, ids in country.groupby('country').groups.items():
        if len(ids) > 1:
            country = country.drop(ids[1:])

    return country.sort_values(by='country')


def extract_concepts():
    concepts = [['name', 'Name', 'string'], ['year', 'Year', 'time'],
                ['country', 'Country / Territory', 'entity_domain'],
                ['cpi', 'Corruption Perceptions Index', 'measure']
                ]
    conc_df = pd.DataFrame(concepts, columns=['concept', 'name', 'concept_type'])

    return conc_df


def extract_datapoints(data):
    dps = data[['wbcode', 'year', 'cpi']].copy()
    dps.columns = ['country', 'year', 'cpi']

    dps['country'] = dps['country'].map(to_concept_id)

    return dps


if __name__ == '__main__':
    print('reading source files...')
    data = cleanup_data(source_dir)

    print('creating concept files...')
    concepts = extract_concepts()
    path = os.path.join(out_dir, 'ddf--concepts.csv')
    concepts.to_csv(path, index=False)

    print('creating entities files...')
    country = extract_entities_country(data)
    path = os.path.join(out_dir, 'ddf--entities--country.csv')
    country.to_csv(path, index=False)

    print('creating datapoints files...')
    datapoint = extract_datapoints(data)
    path = os.path.join(out_dir, 'ddf--datapoints--cpi--by--country--year.csv')
    datapoint.to_csv(path, index=False)

    print('creating index file...')
    create_index_file(out_dir)

    print('Done.')
