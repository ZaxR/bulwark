Design
=======

It's important that ``Bulwark`` not get in your way. Your task is hard enough without a bunch of assertions
cluttering up the logic of the code. And yet, it does help to explicitly state the assumptions fundamental to your analysis.
Decorators provide a nice compromise.

Checks
------

Each check:
- takes a pd.DataFrame as its first argument, with optional additional arguments,
- make an assert about the pd.DataFrame, and
- return the original, unaltered pd.DataFrame

If the assertion fails, an ``AssertionError`` is raised and ``Bulwark``
tries to print out some informative information about where the failure
occurred.

Decorators
----------

Each ``check`` has an auto-magically-generated associated decorator. The decorator simply marshals
arguments, allowing you to make your assertions *outside* the actual logic
of your code. Besides making it quick and easy to add checks to a function, decorators also come with
bonus capabilities, including the ability to enable/disable the check as well as switch from raising an error
to logging a warning.
