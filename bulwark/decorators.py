# -*- coding: utf-8 -*-
import functools
import inspect

import bulwark.checks as ck


class BaseDecorator(object):
    def __init__(self, *args, **kwargs):  # how to take args in decorator..?
        self.enabled = True  # setter to enforce bool would be a lot safer, but challenge w/ decorator
        # self.warn = False ? No - put at func level for all funcs and pass through
        self.params = inspect.getfullargspec(self.check_func).args[1:]

        self.__dict__.update(dict(zip(self.params, args)))
        self.__dict__.update(**kwargs)

    def __call__(self, f):
        @functools.wraps(f)
        def decorated(*args, **kwargs):
            df = f(*args, **kwargs)
            if self.enabled:
                kwargs = {k: v for k, v in self.__dict__.items() if k not in ["check_func", "enabled", "params"]}
                self.check_func(df, **kwargs)
            return df
        return decorated


class HasDtypes(BaseDecorator):
    check_func = staticmethod(ck.has_dtypes)


class HasNoNans(BaseDecorator):
    check_func = staticmethod(ck.has_no_nans)


class HasNoInfs(BaseDecorator):
    check_func = staticmethod(ck.has_no_infs)


class HasNoNegInfs(BaseDecorator):
    check_func = staticmethod(ck.has_no_neg_infs)


class IsMonotonic(BaseDecorator):
    check_func = staticmethod(ck.is_monotonic)


class IsSameAs(BaseDecorator):
    check_func = staticmethod(ck.is_same_as)


class IsShape(BaseDecorator):
    check_func = staticmethod(ck.is_shape)


class OneToMany(BaseDecorator):
    check_func = staticmethod(ck.one_to_many)


class Unique(BaseDecorator):
    check_func = staticmethod(ck.unique)


class UniqueIndex(BaseDecorator):
    check_func = staticmethod(ck.unique_index)


class WithinNStd(BaseDecorator):
    check_func = staticmethod(ck.within_n_std)


class WithinRange(BaseDecorator):
    check_func = staticmethod(ck.within_range)


class WithinSet(BaseDecorator):
    check_func = staticmethod(ck.within_set)


class MultiCheck(BaseDecorator):
    check_func = staticmethod(ck.multi_check)


def verify(func, *args, **kwargs):
    """
    Assert that `func(df, *args, **kwargs)` is true.
    """
    return _verify(func, None, *args, **kwargs)


def verify_all(func, *args, **kwargs):
    """
    Assert that all of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'all', *args, **kwargs)


def verify_any(func, *args, **kwargs):
    """
    Assert that any of `func(*args, **kwargs)` are true.
    """
    return _verify(func, 'any', *args, **kwargs)


def _verify(func, _kind, *args, **kwargs):
    d = {None: ck.verify, 'all': ck.verify_all, 'any': ck.verify_any}
    vfunc = d[_kind]

    def decorate(operation_func):
        @functools.wraps(operation_func)
        def wrapper(*operation_args, **operation_kwargs):
            result = operation_func(*operation_args, **operation_kwargs)
            vfunc(result, func, *args, **kwargs)
            return result
        return wrapper
    return decorate
