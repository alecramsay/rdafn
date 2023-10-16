#!/usr/bin/env python3

"""
UTILITIES
"""

import time
from functools import wraps
from typing import Any, Callable


def time_function(func) -> Callable[..., Any]:
    """A decorator to report execution run time for freestanding functions"""

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        tic: float = time.perf_counter()

        result: Any = func(*args, **kwargs)

        toc: float = time.perf_counter()
        print(f"{func.__name__} = {toc - tic: 0.1f} seconds")

        return result

    return wrapper
