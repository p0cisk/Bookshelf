#!/usr/bin/python
# -*- coding: utf-8 -*-

from functools import wraps
from playhouse.test_utils import count_queries

def count(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        with count_queries() as counter:
            result = func(*args, **kwargs)
        print(counter.count)
        return result
    return wrapper
