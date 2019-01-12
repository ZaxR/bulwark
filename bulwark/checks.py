# -*- coding: utf-8 -*-
"""
Each function in this module should:

- take a pd.DataFrame as its first argument, with optional additional arguments,
- make an assert about the pd.DataFrame, and
- return the original, unaltered pd.DataFrame

"""
import numpy as np
import pandas as pd
import pandas.util.testing as tm
import six

from bulwark.generic import bad_locations, verify, verify_all, verify_any


def is_shape(df, shape):
    """Asserts that `df` is of a known row x column `shape`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        shape (tuple): Shape of `df` as (n_rows, n_columns).
                       Use None or -1 if you don't care about a specific dimension.

    Returns:
        Original `df`.

    """
    try:
        check = np.all(np.equal(df.shape, shape) | (np.equal(shape, [-1, -1]) |
                                                    np.equal(shape, [None, None])))
        assert check
    except AssertionError as e:
        msg = ("Expected shape: {}\n"
               "\t\tActual shape:   {}".format(shape, df.shape))
        e.args = (msg,)
        raise
    return df


def has_no_nans(df, columns=None):
    """Asserts that there are no np.nans in `df`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for np.nans.

    Returns:
        Original `df`.

    """
    if columns is None:
        columns = df.columns
    try:
        assert not df[columns].isnull().values.any()
    except AssertionError as e:
        missing = df[columns].isnull()
        msg = bad_locations(missing)
        e.args = msg
        raise
    return df


def has_no_infs(df, columns=None):
    """Asserts that there are no np.infs in `df`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for np.nans.

    Returns:
        Original `df`.

    """
    if columns is None:
        columns = df.columns
    try:
        assert not df[columns].isin([np.inf]).values.any()
    except AssertionError as e:
        missing = df[columns].isin([np.inf])
        msg = bad_locations(missing)
        e.args = msg
        raise
    return df


def has_no_neg_infs(df, columns=None):
    """Asserts that there are no np.infs in `df`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for np.nans.

    Returns:
        Original `df`.

    """
    if columns is None:
        columns = df.columns
    try:
        assert not df[columns].isin([-np.inf]).values.any()
    except AssertionError as e:
        missing = df[columns].isin([np.inf])
        msg = bad_locations(missing)
        e.args = msg
        raise
    return df


def is_monotonic(df, items=None, increasing=None, strict=False):
    """
    Asserts that the DataFrame is monotonic.

    Parameters
    ==========

    df : Series or DataFrame
    items : dict
        mapping columns to conditions (increasing, strict)
    increasing : None or bool
        None is either increasing or decreasing.
    strict : whether the comparison should be strict

    Returns
    =======
    df : DataFrame
    """
    if items is None:
        items = {k: (increasing, strict) for k in df}

    for col, (increasing, strict) in items.items():
        s = pd.Index(df[col])
        if increasing:
            good = getattr(s, 'is_monotonic_increasing')
        elif increasing is None:
            good = getattr(s, 'is_monotonic') | getattr(s, 'is_monotonic_decreasing')
        else:
            good = getattr(s, 'is_monotonic_decreasing')
        if strict:
            if increasing:
                good = good & (s.to_series().diff().dropna() > 0).all()
            elif increasing is None:
                good = good & ((s.to_series().diff().dropna() > 0).all() |
                               (s.to_series().diff().dropna() < 0).all())
            else:
                good = good & (s.to_series().diff().dropna() < 0).all()
        if not good:
            raise AssertionError
    return df


def unique(df, columns=None):
    """
    Asserts that columns in the DataFrame only have unique values.

    Parameters
    ----------
    df : DataFrame
    columns : list
      list of columns to restrict the check to. If None, check all columns.

    Returns
    -------
    df : DataFrame
      same as the original
    """
    if columns is None:
        columns = df.columns
    for col in columns:
        if not df[col].is_unique:
            raise AssertionError("Column {!r} contains non-unique values".format(col))
    return df


def unique_index(df):
    """
    Assert that the index is unique

    Parameters
    ==========
    df : DataFrame

    Returns
    =======
    df : DataFrame
    """
    try:
        assert df.index.is_unique
    except AssertionError as e:
        e.args = df.index[df.index.duplicated()].unique()
        raise
    return df


def within_set(df, items=None):
    """
    Assert that df is a subset of items

    Parameters
    ==========
    df : DataFrame
    items : dict
      mapping of columns (k) to array-like of values (v) that
      ``df[k]`` is expected to be a subset of

    Returns
    =======
    df : DataFrame
    """
    for k, v in items.items():
        if not df[k].isin(v).all():
            bad = df.loc[~df[k].isin(v), k]
            raise AssertionError('Not in set', bad)
    return df


def within_range(df, items=None):
    """
    Assert that a DataFrame is within a range.

    Parameters
    ==========
    df : DataFame
    items : dict
      mapping of columns (k) to a (low, high) tuple (v)
      that ``df[k]`` is expected to be between.

    Returns
    =======
    df : DataFrame
    """
    for k, (lower, upper) in items.items():
        if (lower > df[k]).any() or (upper < df[k]).any():
            bad = (lower > df[k]) | (upper < df[k])
            raise AssertionError("Outside range", bad)
    return df


def within_n_std(df, n=3):
    """
    Assert that every value is within ``n`` standard
    deviations of its column's mean.

    Parameters
    ==========
    df : DataFame
    n : int
      number of standard deviations from the mean

    Returns
    =======
    df : DataFrame
    """
    means = df.mean()
    stds = df.std()
    inliers = (np.abs(df[means.index] - means) < n * stds)
    if not np.all(inliers):
        msg = bad_locations(~inliers)
        raise AssertionError(msg)
    return df


def has_dtypes(df, items):
    """
    Assert that a DataFrame has ``dtypes``

    Parameters
    ==========
    df: DataFrame
    items: dict
      mapping of columns to dtype.

    Returns
    =======
    df : DataFrame
    """
    dtypes = df.dtypes
    for k, v in items.items():
        if not dtypes[k] == v:
            raise AssertionError("{} has the wrong dtype. Should be ({}), is ({})".format(k, v, dtypes[k]))
    return df


def one_to_many(df, unitcol, manycol):
    """
    Assert that a many-to-one relationship is preserved between two
    columns. For example, a retail store will have have distinct
    departments, each with several employees. If each employee may
    only work in a single department, then the relationship of the
    department to the employees is one to many.

    Parameters
    ==========
    df : DataFrame
    unitcol : str
        The column that encapulates the groups in ``manycol``.
    manycol : str
        The column that must remain unique in the distict pairs
        between ``manycol`` and ``unitcol``

    Returns
    =======
    df : DataFrame

    """
    subset = df[[manycol, unitcol]].drop_duplicates()
    for many in subset[manycol].unique():
        if subset[subset[manycol] == many].shape[0] > 1:
            msg = "{} in {} has multiple values for {}".format(many, manycol, unitcol)
            raise AssertionError(msg)

    return df


def is_same_as(df, df_to_compare, **kwargs):
    """
    Assert that two pandas dataframes are the equal

    Parameters
    ==========
    df : pandas DataFrame
    df_to_compare : pandas DataFrame
    **kwargs : dict
        keyword arguments passed through to panda's ``assert_frame_equal``

    Returns
    =======
    df : DataFrame

    """
    try:
        tm.assert_frame_equal(df, df_to_compare, **kwargs)
    except AssertionError as exc:
        six.raise_from(AssertionError("DataFrames are not equal"), exc)
    return df


def multi_check(df, checks, warn=False):
    error_msgs = []
    for func, params in checks.items():
        try:
            func(df, **params)
        except AssertionError as e:
            error_msgs.append(e)

    if warn and error_msgs:
        print(error_msgs)
        return df
    elif error_msgs:
        raise AssertionError("\n".join(str(i) for i in error_msgs))

    return df
