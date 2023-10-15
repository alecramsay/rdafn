#!/usr/bin/env python3

"""
ANALYZE A PLAN
"""

import pandas as pd

from .datatypes import *


def analyze_plan(
    name: str,
    assignments: list[dict[str, int]],
    data: dict[str, dict[str, int]],
    shapes: pd.Series | pd.DataFrame | Any,
) -> dict[str, int | float]:
    """Analyze a plan."""

    print(f"Analyzing plan {name} ...")

    results: dict[str, int | float] = dict()

    # TODO

    # COMPACTNESS

    # Or construct them from block shapes and a block-assigment file:
    # shapes_path: str = os.path.expanduser(f"{data_dir}/{shapes_file}")
    # blocks_gdf: GeoDataFrame = geopandas.read_file(shapes_path)
    # blocks_df: pd.Series | pd.DataFrame | Any = blocks_gdf[["geometry", "GEOID20"]]
    # del blocks_gdf
    # assert isinstance(blocks_df, pd.DataFrame)

    # plan_path: str = os.path.expanduser(f"{data_dir}/{plan_file}")
    # plan_gdf: GeoDataFrame = geopandas.read_file(plan_path)
    # plan_df: pd.Series | pd.DataFrame | Any = plan_gdf[["GEOID20", "District"]]
    # del plan_gdf
    # assert isinstance(plan_df, pd.DataFrame)

    # blocks_df = blocks_df.merge(
    #     plan_df,
    #     how="left",
    #     left_on="GEOID20",
    #     right_on="GEOID20",
    # )
    # blocks_df = blocks_df[["geometry", "GEOID20", "District"]]
    # assert isinstance(blocks_df, GeoDataFrame)
    # del plan_df

    # districts_df = blocks_df.dissolve(by="District", as_index=False)

    # unsorted_shapes: list[dict] = districts_df.to_dict("records")
    # sorted_shapes: list[dict] = sorted(unsorted_shapes, key=lambda k: k["District"])
    # shapes = [s["geometry"] for s in sorted_shapes]  # discard the id

    pass

    return results


### END ###
