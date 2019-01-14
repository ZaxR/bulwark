# -*- coding: utf-8 -*-
"""
Module for useful generic functions.
"""
from itertools import chain, cycle

import numpy as np
import pandas as pd


#########################
#### ERROR REPORTING ####
#########################

def bad_locations(df):
    """Indicates bad cells in `df`."""
    columns = df.columns
    all_locs = chain.from_iterable(zip(df.index, cycle([col])) for col in columns)
    bad = pd.Series(list(all_locs))[np.asarray(df).ravel(order='F')]
    msg = bad.values

    return msg


def snake_to_camel(snake_str):
    components = snake_str.split('_')
    return ''.join(x.title() for x in components)
