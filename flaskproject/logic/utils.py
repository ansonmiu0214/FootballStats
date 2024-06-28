
# built-ins
import functools
import logging
from typing import Callable

# external
from flask import jsonify


def log_exception(fn: Callable):
    """A function decorator that logs exceptions."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logging.error('footballstats: caught exception', exc_info=e)
            raise
    
    return wrapper


def return_exception_as_json(fn: Callable):
    """A function decorator that suppresses exceptions as Flask-compatible JSON responses
    with 'error' payload."""

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)})

    return wrapper