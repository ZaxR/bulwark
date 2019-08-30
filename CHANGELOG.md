Changelog
==========


<h2>[0.5.0] - 2019-08-18</h2>
**Added**
- Add support for old Engarde function names with deprecation warnings for v0.7.0.
- Add ability to check bulwark version with `bulwark.__version__`
- Add status badges to README.md
- Add Sphinx markdown support and single-source readme, changelog.

**Changed**
- Upgrade Development Status to Beta (from Alpha)
- Update gitignore for venv
- Update contributing documentation
- Single-sourced project version

<h2>[0.4.2] - 2019-07-28</h2>
**Changed**
- Hotfix to allow import bulwark to work.

<h2>[0.4.1] - 2019-07-26</h2>
**Changed**
- Hotfix to allow import bulwark to work.

<h2>[0.4.0] - 2019-07-26</h2>
**Added**
- Add `has_no_x`, `has_no_nones`, and `has_set_within_vals`.

**Changed**
- `has_no_nans` now checks only for np.nans and not also None. Checking for None is available through has_no_nones.

<h2>[0.3.0] - 2019-05-30</h2>
**Added**
- Add `exact_order` param to `has_columns`

**Changed**
- Hotfix for reversed `has_columns` error messages for missing and unexpected columns
- Breaking change to `has_columns` parameter name `exact`, which is now `exact_cols`

<h2>[0.2.0] - 2019-05-29</h2>
**Added**
- Add `has_columns` check, which asserts that the given columns are contained within the df or exactly match the df's columns.
- Add changelog

**Changed**
- Breaking change to rename unique_index to has_unique_index for consistency


<h2>[0.1.2] - 2019-01-13</h2>
**Changed**
- Improve code base to automatically generate decorators for each check
- Hotfix multi_check and unit tests


<h2>[0.1.1] - 2019-01-12</h2>
**Changed**
- Hotfix to setup.py for the sphinx.setup_command.BuildDoc requirement.


<h2>[0.1.0] - 2019-01-12</h2>
**Changed**
- Breaking change to rename unique_index to has_unique_index for consistency
