#!/usr/bin/env python3

"""
LOAD HELPERS
"""

import pandas as pd
import geopandas
from geopandas import GeoDataFrame

from .constants import *
from .readwrite import *


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data."""

    pickle_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "pickle"
    )

    data: dict[str, dict[str, int]] = read_pickle(pickle_path)

    return data


def load_topology(xx: str) -> dict[str, Any]:
    """Load the topology for a state."""

    topo_dir: str = "temp"  # TODO - Point this at the right place.

    topo_path: str = f"{topo_dir}/{xx}_vtd_simple_topo.json"
    # topo_path: str = f"{topo_dir}/{xx}_vtd_topo.json"
    # topo_path: str = f"{topo_dir}/{xx}_vtd_quantized_topo.json"

    topo: dict[str, Any] = read_json(topo_path)

    return topo


# NOTE - Use the topology instead.
def load_shapes(xx: str) -> pd.Series | pd.DataFrame | Any:
    """Load the shapefile for a state."""

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    shapes_file: str = f"tl_2020_{fips}_vtd20"
    shapes_path: str = os.path.abspath(f"{data_dir}/{xx}/{shapes_file}")
    # https://geopandas.org/en/stable/docs/user_guide/io.html
    shapes_path: str = f"zip://{shapes_path}.zip!{shapes_file}"

    precincts_gdf: GeoDataFrame = geopandas.read_file(shapes_path)
    precincts_df: pd.Series | pd.DataFrame | Any = precincts_gdf[
        ["geometry", "GEOID20"]
    ]
    del precincts_gdf
    assert isinstance(precincts_df, pd.DataFrame)

    return precincts_df


def load_plan(plan_file: str) -> list[dict[str, str | int]]:
    """Read a precinct-assignment file."""

    assignments: list[dict[str, str | int]] = read_csv(plan_file, [str, int])

    return assignments


### END ###
