#!/usr/bin/env python3

"""
ANALYZE A PLAN
"""

import pandas as pd
import rdapy as rda

from .constants import *
from .datatypes import *
from .utils import *


@time_function
def analyze_plan(
    name: str,
    assignments: list[dict[str, int]],
    data: dict[str, dict[str, int]],
    shapes: pd.Series | pd.DataFrame | Any,
) -> dict[str, int | float]:
    """Analyze a plan."""

    print(f"Analyzing plan {name} ...")

    ### AGGREGATE DATA BY DISTRICT ###

    total_pop_field: str = census_fields[0]
    total_vap_field: str = census_fields[1]
    white_vap_field: str = census_fields[2]
    hispanic_vap_field: str = census_fields[3]
    black_vap_field: str = census_fields[4]
    native_vap_field: str = census_fields[5]
    asian_vap_field: str = census_fields[6]
    pacific_vap_field: str = census_fields[7]
    minority_vap_field: str = census_fields[8]

    tot_votes_field: str = election_fields[0]
    rep_votes_field: str = election_fields[1]
    dem_votes_field: str = election_fields[2]
    oth_votes_field: str = election_fields[3]

    total_pop: int = 0
    pop_by_district: defaultdict[int | str, int] = defaultdict(int)

    d_by_district: defaultdict[int | str, int] = defaultdict(int)
    tot_by_district: defaultdict[int | str, int] = defaultdict(int)
    d_statewide: int = 0
    tot_statewide: int = 0

    for row in assignments:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        district: int = row["DISTRICT"] if "DISTRICT" in row else row["District"]

        pop: int = data[precinct][total_pop_field]
        pop_by_district[district] += pop
        total_pop += pop

        d: int = data[precinct][dem_votes_field]
        tot: int = (
            data[precinct][dem_votes_field] + data[precinct][rep_votes_field]
        )  # NOTE - Two-party vote total

        d_by_district[district] += d
        d_statewide += d

        tot_by_district[district] += tot
        tot_statewide += tot

    Vf: float = d_statewide / tot_statewide
    Vf_array: list[float] = [
        d / tot for d, tot in zip(d_by_district.values(), tot_by_district.values())
    ]

    pass

    ### CREATE DISTRICT SHAPES ###

    # TODO

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

    ### CALCULATE ANALYTICS ###

    scorecard: dict[str, int | float] = dict()

    # Population deviation

    max_pop: int = max(pop_by_district.values())
    min_pop: int = min(pop_by_district.values())
    target_pop: int = int(total_pop / len(pop_by_district))

    deviation: float = rda.calc_population_deviation(max_pop, min_pop, target_pop)
    scorecard["popdev"] = deviation

    # Partisan metrics

    partisan_metrics: dict = rda.calc_partisan_metrics(Vf, Vf_array)

    bias_metrics: dict = dict(partisan_metrics["bias"])
    bias_metrics.pop("rvPoints", None)
    bias_metrics.pop("gamma", None)
    bias_metrics.pop("gSym", None)
    scorecard.update(bias_metrics)

    responsiveness_metrics: dict = dict(partisan_metrics["responsiveness"])
    scorecard.update(responsiveness_metrics)

    scorecard.update({"averageDVf": partisan_metrics["averageDVf"]})
    scorecard.update({"averageRVf": partisan_metrics["averageRVf"]})

    # TODO - Minority

    # TODO - Compactness

    # TODO - Splitting

    # TODO - Ratings

    return scorecard


### END ###
