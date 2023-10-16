#!/usr/bin/env python3

"""
LOAD HELPERS
"""

import pandas as pd
import geopandas
from geopandas import GeoDataFrame

from .constants import *
from .readwrite import *
from .datatypes import *


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data."""

    pickle_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "pickle"
    )

    data: dict[str, dict[str, int]] = read_pickle(pickle_path)

    return data


def load_shapes(xx: str) -> pd.Series | pd.DataFrame | Any:
    """Load the shapefile for a state."""

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    # https://geopandas.org/en/stable/docs/user_guide/io.html
    shapes_file: str = f"tl_2020_{fips}_vtd20"
    shapes_path: str = os.path.expanduser(f"{data_dir}/{xx}/{shapes_file}")
    # zipfile: str = "zip://" + shapes_path + f"!data/{shapes_file}.shp" # TODO

    blocks_gdf: GeoDataFrame = geopandas.read_file(shapes_path)
    blocks_df: pd.Series | pd.DataFrame | Any = blocks_gdf[["geometry", "GEOID20"]]
    del blocks_gdf
    assert isinstance(blocks_df, pd.DataFrame)

    return blocks_df


def load_plan(plan_file: str, name: Optional[str] = None) -> Plan:
    """Read a precinct-assignment file."""

    plan: Plan = Plan(plan_file, name)

    return plan


### END ###
