Bulwark's Documentation
========================================

Bulwark is a package for convenient property-based testing of pandas dataframes, supported for Python 3.5+.

Documentation: https://bulwark.readthedocs.io/en/latest/index.html

This project was heavily influenced by the no-longer-supported [Engarde](https://github.com/TomAugspurger/engarde) library
by Tom Augspurger (thanks for the head start, Tom!), which itself was modeled after
the R library [assertr](https://github.com/ropenscilabs/assertr).


Why?
====

Data are messy, and pandas is one of the go-to libraries for analyzing tabular data.
In the real world, data analysts and scientists often feel like they don't have the time
or energy to think of and write tests for their data. Bulwark's goal is to let you check
that your data meets your assumptions of what it should look like at any (and every) step
in your code, without making you work too hard.


Usage
=====

Bulwark comes with checks for many of the common assumptions you might want to validate
for the functions that make up your ETL pipeline, and lets you toss those checks as decorators
on the functions you're already writing:

```python
   import bulwark.decorators as dc

   @dc.IsShape(-1, 10)
   @dc.IsMonotonic(strict=True)
   @dc.HasNoNans()
   def compute(df):
       # complex operations to determine result
       ...
       return result_df
```
Still want to have more robust test files? Bulwark's got you covered there, too, with importable functions.

```python
   import bulwark.checks as ck

   df.pipe(ck.has_no_nans()) 
```
Won't I have to go clean up all those decorators when I'm ready to go to production?
Nope - just toggle the built-in debug_mode flag available for every decorator.

```python
   @dc.IsShape((3, 2), debug_mode=False)
   def compute(df):
       # complex operations to determine result
       ...
       return result_df
```
What if the test I want isn't part of the library?
Use the build-in `verify`, `verify_all`, `veryify_any` functions/decorators to use your own
custom function!

```python
   def custom_check_func(df):
       # some really special check
       ...
       return df

   @dc.verify_all(custom_check_func)
   def compute():
       # complex operations to determine result
       ...
       return result_df
```
Check out [examples](https://bulwark.readthedocs.io/en/latest/examples.html) to see more advanced usage.


Roadmap
=======

- Fix bug: MultiCheck is broken
- Add to pypi
- Add travis build server
- Implement class factory
- Fix/Improve documentation
  - inherit BaseDecorator and the functions' docstrings w/ __doc__
  - rewrite design.rst and examples.rst
  - Demo how to use with read files from csv; write func to import, decorate with dc.funcs
- Refactor warn functionality, adding to all functions/decorators
  - Add warn hook for desired effect if not error
- Improve error message outputs
  - Possibly JSON format
- Add functions for:
  - has_col_order,
  - has_cols,
  - Add check for object type columns that all values are of a python type (e.g. all str),
  - Check incrementing/complete index