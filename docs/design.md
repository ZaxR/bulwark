Design
======

It's important that `Bulwark` does not get in your way. Your task is hard
enough without a bunch of assertions cluttering up the logic of the
code. And yet, it does help to explicitly state the assumptions
fundamental to your analysis. Decorators provide a nice compromise.

Checks
------

Each check:

- takes a pd.DataFrame as its first argument, with optional additional
  arguments,
- makes an assert about the pd.DataFrame, and
- returns the original, unaltered pd.DataFrame.

If the assertion fails, an `AssertionError` is raised and `Bulwark`
tries to print out some informative summary about where the failure
occurred.

Decorators
----------

Each `check` has an auto-magically-generated associated decorator. The
decorator simply marshals arguments, allowing you to make your
assertions *outside* the actual logic of your code. Besides making it
quick and easy to add checks to a function, decorators also come with
bonus capabilities, including the ability to enable/disable the check as
well as to switch from raising an error to just logging a warning.
