Bulwark's Documentation
========================================
<a href="https://pypi.org/project/bulwark/"><img src="https://img.shields.io/pypi/dm/bulwark?style=for-the-badge" alt="downloads" /></a>  

<a href="https://pypi.org/project/bulwark/"><img src="https://img.shields.io/pypi/v/bulwark?style=for-the-badge" alt="latest release" /></a>
<a href="https://pypi.org/project/bulwark/"><img src="https://img.shields.io/pypi/pyversions/bulwark?style=for-the-badge" alt="supported python versions" /></a>
<a href="https://pypi.org/project/bulwark/"><img src="https://img.shields.io/pypi/status/bulwark?style=for-the-badge" alt="package status" /></a>
<a href="https://anaconda.org/conda-forge/bulwark"><img src="https://img.shields.io/conda/pn/conda-forge/bulwark?style=for-the-badge" alt="conda" /></a>
<a href="https://github.com/ZaxR/bulwark/blob/master/LICENSE"><img src="https://img.shields.io/pypi/l/bulwark?style=for-the-badge" alt="license" /></a>

<a href="https://travis-ci.com/ZaxR/bulwark"><img src="https://img.shields.io/travis/com/ZaxR/bulwark?style=for-the-badge" alt="travis build status" /></a>
<a href="https://bulwark.readthedocs.io/en/latest/"><img src="https://img.shields.io/readthedocs/bulwark/latest?style=for-the-badge" alt="docs build status" /></a>
<a href="https://codecov.io/gh/ZaxR/bulwark"><img src="https://img.shields.io/codecov/c/github/zaxr/bulwark?style=for-the-badge&token=79c0ebb7eba84f56845fbc3073a0cb18" alt="coverage status" /></a>

Bulwark is a package for convenient property-based testing of pandas dataframes,
supported for Python 3.5+.

Documentation: https://bulwark.readthedocs.io/en/latest/index.html

This project was heavily influenced by the no-longer-supported [Engarde](https://github.com/TomAugspurger/engarde) library
by Tom Augspurger(thanks for the head start, Tom!),
which itself was modeled after
the R library [assertr](https://github.com/ropenscilabs/assertr).

Why?
====

Data are messy, and pandas is one of the go-to libraries for analyzing tabular data.
In the real world,
data analysts and scientists often feel like they don't have the time or energy
to think of and write tests for their data.
Bulwark's goal is to let you check
that your data meets your assumptions of what it should look like
at any (and every) step in your code,
without making you work too hard.

Installation
=============

```bash
pip install bulwark
```

or

```bash
conda install -c conda-forge bulwark
```

Usage
=====

Bulwark comes with checks for many of the common assumptions you might want to validate
for the functions that make up your ETL pipeline,
and lets you toss those checks as decorators
on the functions you're already writing:

```python
    import bulwark.decorators as dc

    @dc.IsShape((-1, 10))
    @dc.IsMonotonic(strict=True)
    @dc.HasNoNans()
    def compute(df):
        # complex operations to determine result
        ...
    return result_df
```

Still want to have more robust test files?
Bulwark's got you covered there, too, with importable functions.

```python
    import bulwark.checks as ck

    df.pipe(ck.has_no_nans())
```

Won't I have to go clean up all those decorators when I'm ready to go to production?
Nope - just toggle the built-in "enabled" flag available for every decorator.

```python
    @dc.IsShape((3, 2), enabled=False)
    def compute(df):
        # complex operations to determine result
        ...
    return result_df
```

What if the test I want isn't part of the library?
Use the built-in `CustomCheck` to use your own custom function!

```python
    def len_longer_than(df, l):
        if len(df) <= l:
            raise AssertionError("df is not as long as expected.")
        return df

    @dc.CustomCheck(len_longer_than, df=df, l=6)
    def append_a_df(df, df2):
        return df.append(df2, ignore_index=True)

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df2 = pd.DataFrame({"a": [1, np.nan, 3, 4], "b": [4, 5, 6, 7]})

    append_a_df(df, df2)
```

What if I want to run a lot of tests and want to see all the errors at once?
You can use the built-in `MultiCheck`.
It will collect all of the errors
and either display a warning message of throw an exception based on the `warn` flag.
You can even use custom functions with MultiCheck:

```python
    def len_longer_than(df, l):
        if len(df) <= l:
            raise AssertionError("df is not as long as expected.")
        return df

    # `checks` takes a dict of function: dict of params for that function.
    # Note that those function params EXCLUDE df.
    # Also note that when you use MultiCheck, there's no need to use CustomCheck - just feed in the function.
    @dc.MultiCheck(checks={ck.has_no_nans: {"columns": None},
                           len_longer_than: {"l": 6}},
                   warn=False)
    def append_a_df(df, df2):
        return df.append(df2, ignore_index=True)

    df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
    df2 = pd.DataFrame({"a": [1, np.nan, 3, 4], "b": [4, 5, 6, 7]})

    append_a_df(df, df2)
```

See [examples](https://bulwark.readthedocs.io/en/latest/examples.html) to see more advanced usage.

## Contributing

Bulwark is always looking for new contributors!
We work hard to make contributing as easy as possible,
and previous open source experience is not required!
Please see [contributing.md](docs/contributing.md) for how to get started.

Thank you to all our past contributors, especially these folks:  
[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/0)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/0)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/1)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/1)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/2)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/2)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/3)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/3)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/4)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/4)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/5)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/5)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/6)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/6)[![](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/images/7)](https://sourcerer.io/fame/ZaxR/ZaxR/bulwark/links/7)
