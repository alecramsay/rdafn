#!/usr/bin/env python3

"""
TYPES
"""

from typing import Optional

from .readwrite import *


class Plan:
    """A named plan from precinct-assignment file"""

    name: str
    assignments: list[dict[str, int]]

    def __init__(self, rel_path: str, name: Optional[str] = None) -> None:
        self.name = name if name else FileSpec(rel_path).name
        self.assignments: list[dict[str, int]] = read_csv(rel_path, [str, int])


### END ###
