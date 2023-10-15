#!/usr/bin/env python3

"""
LOAD HELPERS
"""

from .constants import *
from .readwrite import *


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data."""

    pickle_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "pickle"
    )

    data: dict[str, dict[str, int]] = read_pickle(pickle_path)

    return data


def load_shapes(xx: str):
    """Load the shapefile for a state."""

    # TODO

    pass


def load_plan(plan_file: str) -> list[dict[str, int]]:
    """Read a precinct-assignment file."""

    precinct_assignments: list[dict[str, int]] = read_csv(plan_file, [str, int])

    return precinct_assignments


### END ###
