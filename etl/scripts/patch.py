# -*- coding: utf-8 -*-

import pandas as pd
import etl
import os

out_dir = etl.out_dir


def remove_duplicated_geo():
    """remove duplicated geo entity for Democratic Republic of the Congo"""
    geo = pd.read_csv(os.path.join(out_dir, 'ddf--entities--country.csv'))
    df = pd.read_csv(os.path.join(out_dir, 'ddf--datapoints--cpi--by--country--year.csv'))

    geo = geo.set_index('country')
    geo = geo.drop('democratic_republic_of_congo')

    df.loc[df.country=='democratic_republic_of_congo', 'country'] = 'cod'

    geo.to_csv(os.path.join(out_dir, 'ddf--entities--country.csv'))
    df.to_csv(os.path.join(out_dir, 'ddf--datapoints--cpi--by--country--year.csv'),
              float_format='%.15g',
              index=False)
