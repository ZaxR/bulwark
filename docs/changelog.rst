Changelog
--------------

**[0.4.2] - 2019-07-28**
Changed
- Hotfix to allow import bulwark to work.

**[0.4.1] - 2019-07-26**
Changed
- Hotfix to allow import bulwark to work.

**[0.4.0] - 2019-07-26**
Added
- Add `has_no_x`, `has_no_nones`, and `has_set_within_vals`.

Changed
- `has_no_nans` now checks only for np.nans and not also None. Checking for None is available through has_no_nones.

**[0.3.0] - 2019-05-30**
Added
- Add `exact_order` param to `has_columns`

Changed
- Hotfix for reversed `has_columns` error messages for missing and unexpected columns
- Breaking change to `has_columns` parameter name `exact`, which is now `exact_cols`

**[0.2.0] - 2019-05-29**
Added
- Add `has_columns` check, which asserts that the given columns are contained within the df or exactly match the df's columns.
- Add changelog

Changed
- Breaking change to rename unique_index to has_unique_index for consistency


**[0.1.2] - 2019-01-13**
Changed
- Improve code base to automatically generate decorators for each check
- Hotfix multi_check and unit tests


**[0.1.1] - 2019-01-12**
Changed
- Hotfix to setup.py for the sphinx.setup_command.BuildDoc requirement.


**[0.1.0] - 2019-01-12**
Changed
- Breaking change to rename unique_index to has_unique_index for consistency