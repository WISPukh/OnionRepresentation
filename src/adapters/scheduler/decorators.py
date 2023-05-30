import functools
import logging

from exceptions import InternalServerError


def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except InternalServerError as exc:
                logging.error(exc)
                if cancel_on_failure:
                    ...
        return wrapper

    return catch_exceptions_decorator
