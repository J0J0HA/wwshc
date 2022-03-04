from typing import *


class Cache:
    __doc__ = """

    """

    cache: Dict[AnyStr, Any] = {}
    EXTRA: str = "__EXTRA__"
    SKIP: str = "__SKIP__"
    C_SKIP: dict = {EXTRA: SKIP}
    RESET: str = "__RESET__"
    C_RESET: str = {EXTRA: RESET}

    def cached(self, ignore_args: bool = False, remove_first: bool = False) -> Callable:
        def decorator(func: Callable) -> Callable:
            if ignore_args is True:
                def wrapper(*args: Tuple, **kwargs: Dict[AnyStr, Any]) -> Any:
                    if "__CACHE__" in kwargs:
                        if kwargs["__CACHE__"] == "__SKIP__":
                            kwargs.pop("__CACHE__")
                            return func(*args, **kwargs)
                        if kwargs["__CACHE__"] == "__RESET__":
                            kwargs.pop("__CACHE__")
                            self.clear(repr(func.__module__ + "." + func.__name__))
                    if not repr(func.__module__ + "." + func.__name__) in self.cache:
                        self.cache[repr(func.__module__ + "." + func.__name__)] = func(*args, **kwargs)
                    return self.cache[repr(func.__module__ + "." + func.__name__)]
            else:
                def wrapper(*args: Tuple, **kwargs: Dict[AnyStr, Any]) -> Any:
                    altargs = args
                    if remove_first:
                        try:
                            tuplist = list(altargs)
                            tuplist.pop(0)
                            altargs = tuple(tuplist)
                        except IndexError:
                            pass
                    if "__EXTRA__" in kwargs:
                        if kwargs["__EXTRA__"] == "__SKIP__":
                            kwargs.pop("__EXTRA__")
                            return func(*args, **kwargs)
                        if kwargs["__EXTRA__"] == "__RESET__":
                            kwargs.pop("__EXTRA__")
                            self.clear(repr([func.__module__ + "." + func.__name__, altargs, kwargs, ]))
                    if not repr([func.__module__ + "." + func.__name__, altargs, kwargs, ]) in self.cache:
                        self.cache[repr([func.__module__ + "." + func.__name__, altargs, kwargs, ])] = func(*args, **kwargs)
                    return self.cache[repr([func.__module__ + "." + func.__name__, altargs, kwargs, ])]
            return wrapper
        return decorator

    def cached_as(self, key: AnyStr, ignore_args: bool = False, remove_first: bool = False):
        if not isinstance(key, str): key = repr(str)

        def decorator(func: Callable) -> Callable:
            if ignore_args:
                def wrapper(*args: Tuple, **kwargs: Dict[AnyStr, Any]) -> Any:
                    if remove_first:
                        try:
                            tuplist = list(args)
                            tuplist.pop(0)
                            args = tuple(tuplist)
                        except IndexError:
                            pass
                    if "__EXTRA__" in kwargs:
                        if kwargs["__EXTRA__"] == "__SKIP__":
                            kwargs.pop("__EXTRA__")
                            return func(*args, **kwargs)
                        if kwargs["__EXTRA__"] == "__RESET__":
                            kwargs.pop("__EXTRA__")
                            self.clear(key)
                    if not key in self.cache:
                        self.cache[key] = func(*args, **kwargs)
                    return self.cache[key]
            else:
                def wrapper(*args: Tuple, **kwargs: Dict[AnyStr, Any]) -> Any:
                    altargs = args
                    if remove_first:
                        try:
                            tuplist = list(altargs)
                            tuplist.pop(0)
                            altargs = tuple(tuplist)
                        except IndexError:
                            pass
                    if "__EXTRA__" in kwargs:
                        if kwargs["__EXTRA__"] == "__SKIP__":
                            kwargs.pop("__EXTRA__")
                            return func(*args, **kwargs)
                        if kwargs["__EXTRA__"] == "__RESET__":
                            kwargs.pop("__EXTRA__")
                            self.clear(repr([key, altargs, kwargs, ]))
                    if not repr([key, altargs, kwargs, ]) in self.cache:
                        self.cache[repr([key, altargs, kwargs, ])] = func(*args, **kwargs)
                    return self.cache[repr([key, altargs, kwargs, ])]
            return wrapper
        return decorator

    def clear(self, key: [AnyStr, None] = None) -> None:
        if key is not None:
            self.cache.pop(key)
        else:
            self.cache = {}

cache = Cache()
