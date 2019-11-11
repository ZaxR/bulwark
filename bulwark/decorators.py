"""Generates decorators for each check in `checks.py`."""
import functools
import sys
from inspect import getfullargspec, getmembers, isfunction

import bulwark.checks as ck
from bulwark.generic import snake_to_camel


class BaseDecorator(object):
    def __init__(self, *args, **kwargs):
        self.enabled = kwargs.pop("enabled", True)  # setter to enforce bool would be a lot safer
        # self.warn = False ? No - put at func level for all funcs and pass through

        self.check_func_params = dict(
            zip(getfullargspec(self.check_func).args[1:], args))
        self.check_func_params.update(**kwargs)

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            df = f(*args, **kwargs)
            if self.enabled:
                self.check_func(df, **self.check_func_params)
            return df
        return decorated


def decorator_factory(decorator_name, func):
    """Takes in a function and outputs a class that can be used as a decorator."""
    class decorator_name(BaseDecorator):
        check_func = staticmethod(func)

    return decorator_name


# Automatically creates decorators for each function in bulwark.checks
this_module = sys.modules[__name__]
check_functions = [func[1]
                   for func in getmembers(ck, isfunction)
                   if func[1].__module__ == 'bulwark.checks']

for func in check_functions:
    decorator_name = snake_to_camel(func.__name__)
    setattr(this_module, decorator_name, decorator_factory(decorator_name, func))


class CustomCheck:
    """
    Notes:
        - This code is purposefully located below the auto-generation of decorators,
          so this overwrites the auto-generated CustomCheck.
        - `CustomCheck`'s __init__ and __call__ diverge from `BaseDecorator`,
          since the check_func needs to be set by the user at creation time.

    TODO: Work this into BaseDecorator?

    """

    def __init__(self, *args, **kwargs):
        self.enabled = kwargs.pop("enabled", True)  # setter to enforce bool would be a lot safer
        # self.warn = False ? No - put at func level for all funcs and pass through

        self.check_func = kwargs.get("check_func")
        if self.check_func:
            check_func_args = args
        else:
            self.check_func = args[0]
            check_func_args = args[1:]

        self.check_func_params = dict(
            zip(getfullargspec(self.check_func).args[1:], check_func_args))
        self.check_func_params.update(**kwargs)

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            df = f(*args, **kwargs)
            if self.enabled:
                # differs from BaseDecorator
                ck.custom_check(df, self.check_func, **self.check_func_params)
            return df
        return decorated
