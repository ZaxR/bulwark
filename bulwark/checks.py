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

from bulwark.generic import bad_locations


def has_columns(df, columns, exact_cols=False, exact_order=False):
    """Asserts that `df` has ``columns``

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list or tuple): Columns that are expected to be in ``df``.
        exact_cols (bool): Whether or not ``columns`` need to be the only columns in ``df``.
        exact_order (bool): Whether or not ``columns`` need to be in the same order as the columns in ``df``.

    Returns:
        Original `df`.

    """
    df_cols = df.columns
    msg = []

    missing_cols = list(set(columns).difference(df_cols))
    if missing_cols:
        msg.append("`df` is missing columns: {}.".format(missing_cols))

    if exact_cols:
        unexpected_extra_cols = list(set(df_cols).difference(columns))
        if unexpected_extra_cols:
            msg.append("`df` has extra columns: {}.".format(unexpected_extra_cols))

    if exact_order:
        if missing_cols:
            msg.append("`df` column order does not match given `columns` order, because columns are missing.")
        else:
            # idx_order = [columns.index(df.columns[i]) for i in range(len(columns))]
            idx_order = []
            for i in range(len(columns)):
                try:
                    idx_order.append(columns.index(df.columns[i]))
                except ValueError:
                    pass
            if idx_order != sorted(idx_order):
                msg.append("`df` column order does not match given `columns` order.")

    if msg:
        raise AssertionError(" ".join(msg))

    return df


def has_no_x(df, values=None, columns=None):
    """Asserts that there are no user-specified `values` in `df`'s `columns`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        values (list): A list of values to check for in the pd.DataFrame.
        columns (list): A subset of columns to check for `values`.

    Returns:
        Original `df`.

    """
    values = values if values is not None else []
    columns = columns if columns is not None else df.columns

    try:
        assert not df[columns].isin(values).values.any()
    except AssertionError as e:
        missing = df[columns].isin(values)
        msg = bad_locations(missing)
        e.args = msg
        raise
    return df


def has_no_nans(df, columns=None):
    """Asserts that there are no np.nans in `df`.

    This is a convenience wrapper for `has_no_x`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for np.nans.

    Returns:
        Original `df`.

    """
    return has_no_x(df, values=[np.nan], columns=columns)


def has_no_nones(df, columns=None):
    """Asserts that there are no Nones in `df`.

    This is a convenience wrapper for `has_no_x`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for Nones.

    Returns:
        Original `df`.

    """
    return has_no_x(df, values=[None], columns=columns)


def has_no_infs(df, columns=None):
    """Asserts that there are no np.infs in `df`.

    This is a convenience wrapper for `has_no_x`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for np.infs.

    Returns:
        Original `df`.

    """
    return has_no_x(df, values=[np.inf], columns=columns)


def has_no_neg_infs(df, columns=None):
    """Asserts that there are no np.infs in `df`.

    This is a convenience wrapper for `has_no_x`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for -np.infs.

    Returns:
        Original `df`.

    """
    return has_no_x(df, values=[-np.inf], columns=columns)


def has_set_within_vals(df, items):
    """Asserts that all given values are found in columns' values.

    In other words, the given values in the `items` dict should all be a subset of
    the values found in the associated column in `df`.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        items (dict): Mapping of columns to values excepted to be found within them.

    Returns:
        Original `df`.

    Examples:
        The following check will pass, since df['a'] contains each of 1 and 2:

        >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': ['a', 'b', 'c']})
        >>> ck.has_set_within_vals(df, items={"a": [1, 2]})

        The following check will fail, since df['b'] doesn't contain each of "a" and "d":

        >>> df = pd.DataFrame({'a': [1, 2, 3], 'b': ['a', 'b', 'c']})
        >>> ck.has_set_within_vals(df, items={"a": [1, 2], "b": ["a", "d"]})

    """
    bad_cols_vals = {}

    for col, vals in items.items():
        missing_vals = np.setdiff1d(vals, df[col].unique(), assume_unique=True).tolist()
        if missing_vals:
            bad_cols_vals.update({col: missing_vals})

    if bad_cols_vals:
        raise AssertionError("The following column: value pairs are missing: {}".format(bad_cols_vals))

    return df


def has_unique_index(df):
    """Asserts that `df`'s index is unique.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.

    Returns:
        Original `df`.

    """
    try:
        assert df.index.is_unique
    except AssertionError as e:
        e.args = df.index[df.index.duplicated()].unique()
        raise

    return df


def is_monotonic(df, items=None, increasing=None, strict=False):
    """Asserts that the `df` is monotonic.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        items (dict): Mapping of columns to conditions (increasing, strict)
        increasing (bool, None): None is either increasing or decreasing.
        strict (bool): Whether the comparison should be strict.

    Returns:
        Original `df`.

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


def unique(df, columns=None):
    """Asserts that columns in `df` only have unique values.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        columns (list): A subset of columns to check for uniqueness of row values.

    Returns:
        Original `df`.

    """
    if columns is None:
        columns = df.columns
    for col in columns:
        if not df[col].is_unique:
            raise AssertionError("Column {!r} contains non-unique values".format(col))
    return df


def within_set(df, items=None):
    """Asserts that `df` is a subset of items.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        items (dict): Mapping of columns (col) to array-like of values (v) that
                      ``df[col]`` is expected to be a subset of.

    Returns:
        Original `df`.

    """
    for col, v in items.items():
        if not df[col].isin(v).all():
            bad = df.loc[~df[col].isin(v), col]
            raise AssertionError('Not in set', bad)
    return df


def within_range(df, items=None):
    """Asserts that `df` is within a range.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        items (dict): Mapping of columns (col) to a (low, high) tuple (v) that
                      ``df[col]`` is expected to be between.

    Returns:
        Original `df`.

    """
    for col, (lower, upper) in items.items():
        if (lower > df[col]).any() or (upper < df[col]).any():
            bad = (lower > df[col]) | (upper < df[col])
            raise AssertionError("Outside range", bad)
    return df


def within_n_std(df, n=3):
    """Asserts that every value is within ``n`` standard deviations of its column's mean.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        n (int): Number of standard deviations from the mean.

    Returns:
        Original `df`.

    """
    means = df.mean()
    stds = df.std()
    inliers = (np.abs(df[means.index] - means) < n * stds)
    if not np.all(inliers):
        msg = bad_locations(~inliers)
        raise AssertionError(msg)
    return df


def has_dtypes(df, items):
    """Asserts that `df` has ``dtypes``

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        items (dict): Mapping of columns to dtype.

    Returns:
        Original `df`.

    """
    dtypes = df.dtypes
    for col, dtype in items.items():
        if not dtypes[col] == dtype:
            raise AssertionError("{} has the wrong dtype. Should be ({}), is ({})".format(col, dtype, dtypes[col]))
    return df


def one_to_many(df, unitcol, manycol):
    """Asserts that a many-to-one relationship is preserved between two columns.

    For example, a retail store will have have distinct departments, each with several employees.
    If each employee may only work in a single department, then the relationship of the
    department to the employees is one to many.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        unitcol (str): The column that encapulates the groups in ``manycol``.
        manycol (str): The column that must remain unique in the distict pairs
                       between ``manycol`` and ``unitcol``.

    Returns:
        Original `df`.

    """
    subset = df[[manycol, unitcol]].drop_duplicates()
    for many in subset[manycol].unique():
        if subset[subset[manycol] == many].shape[0] > 1:
            msg = "{} in {} has multiple values for {}".format(many, manycol, unitcol)
            raise AssertionError(msg)

    return df


def is_same_as(df, df_to_compare, **kwargs):
    """Asserts that two pd.DataFrames are equal.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        df_to_compare (pd.DataFrame): A second pd.DataFrame.
        **kwargs (dict): Keyword arguments passed through to pandas' ``assert_frame_equal``.

    Returns:
        Original `df`.

    """
    try:
        tm.assert_frame_equal(df, df_to_compare, **kwargs)
    except AssertionError as exc:
        six.raise_from(AssertionError("DataFrames are not equal"), exc)
    return df


def multi_check(df, checks, warn=False):
    """Asserts that all checks pass.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        checks (dict): Mapping of check functions to parameters for those check functions.
        warn (bool): Indicates whether an error should be raised
                     or only a warning notification should be displayed.
                     Default is to error.

    Returns:
        Original `df`.

    """
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


def custom_check(check_func, df, *args, **kwargs):
    """Assert that `check(df, *args, **kwargs)` is true.

    Args:
        df (pd.DataFrame): Any pd.DataFrame.
        check_func (function): A function taking `df`, `*args`, and `**kwargs`.
                               Should raise AssertionError if check not passed.

    Returns:
        Original `df`.

    """
    try:
        check_func(df, *args, **kwargs)
    except AssertionError as e:
        msg = "{} is not true.".format(check_func.__name__)
        e.args = (msg,)
        raise

    return df
