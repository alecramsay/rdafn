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


class GeoID:
    """Parse 15-character GeoIDs into their component parts."""

    def __init__(self, id: str) -> None:
        self.state: str = id[0:2]
        self.county: str = id[0:5]  # id[2:5]
        self.tract: str = id[0:11]  # id[5:11]
        self.bg: str = id[0:12]  # id[11:12]
        self.block: str = id  # id[12:15]


### END ###
