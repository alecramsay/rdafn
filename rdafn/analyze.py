#!/usr/bin/env python3

"""
ANALYZE A PLAN
"""

import pandas as pd
from geopandas import GeoDataFrame

import rdapy as rda

from .constants import *
from .datatypes import *
from .utils import *


@time_function
def analyze_plan(
    name: str,
    assignments: list[dict[str, int]],
    data: dict[str, dict[str, int]],
    shapes_df: pd.Series | pd.DataFrame | Any,
    n_districts: int,
    compactness: bool = True,
) -> dict[str, int | float]:
    """Analyze a plan."""

    print(f"Analyzing plan {name} ...")

    ### FIELD NAMES ###

    total_pop_field: str = census_fields[0]
    total_vap_field: str = census_fields[1]
    white_vap_field: str = census_fields[2]
    hispanic_vap_field: str = census_fields[3]
    black_vap_field: str = census_fields[4]
    native_vap_field: str = census_fields[5]
    asian_vap_field: str = census_fields[6]
    pacific_vap_field: str = census_fields[7]
    minority_vap_field: str = census_fields[8]

    total_votes_field: str = election_fields[0]
    rep_votes_field: str = election_fields[1]
    dem_votes_field: str = election_fields[2]
    oth_votes_field: str = election_fields[3]

    ### AGGREGATE DATA BY DISTRICT ###

    # For population deviation

    total_pop: int = 0
    pop_by_district: defaultdict[int | str, int] = defaultdict(int)

    # For partisan metrics

    total_votes: int = 0
    total_d_votes: int = 0
    d_by_district: defaultdict[int | str, int] = defaultdict(int)
    tot_by_district: defaultdict[int | str, int] = defaultdict(int)

    # For minority opportunity metrics

    demos_totals: dict[str, float] = defaultdict(int)
    demos_by_district: list[dict[str, float]] = [
        dict(demos_totals) for _ in range(n_districts)
    ]

    # For county-district splitting

    # NOTE - This could be done once for all plans being analyzed.
    counties: set[str] = set()
    districts: set[int | str] = set()

    for row in assignments:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        district: int = row["DISTRICT"] if "DISTRICT" in row else row["District"]

        county: str = GeoID(precinct).county[2:]

        counties.add(county)
        districts.add(district)

    county_to_index: dict[str, int] = {county: i for i, county in enumerate(counties)}
    district_to_index: dict[int | str, int] = {
        district: i for i, district in enumerate(districts)
    }
    # End NOTE

    CxD: list[list[float]] = [[0.0] * len(counties) for _ in range(len(districts))]

    for row in assignments:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        district: int = row["DISTRICT"] if "DISTRICT" in row else row["District"]

        # For population deviation

        pop: int = data[precinct][total_pop_field]
        pop_by_district[district] += pop
        total_pop += pop

        # For partisan metrics

        d: int = data[precinct][dem_votes_field]
        tot: int = (
            data[precinct][dem_votes_field] + data[precinct][rep_votes_field]
        )  # NOTE - Two-party vote total

        d_by_district[district] += d
        total_d_votes += d

        tot_by_district[district] += tot
        total_votes += tot

        # For minority opportunity metrics

        # TODO

        # For county-district splitting

        county: str = GeoID(precinct).county[2:]

        i: int = district_to_index[district]
        j: int = county_to_index[county]

        CxD[i][j] += pop

    ### CREATE DISTRICT SHAPES FOR COMPACTNESS ###

    shapes: list[Any] = list()  # HACK
    if compactness:
        plan_df: pd.DataFrame = pd.DataFrame(assignments)
        shape_geoid_field: str = "GEOID" if "GEOID" in plan_df.columns else "GEOID20"
        shape_district_field: str = (
            "DISTRICT" if "DISTRICT" in plan_df.columns else "District"
        )
        # assert isinstance(plan_df, pd.DataFrame) # TODO

        shapes_df = shapes_df.merge(
            plan_df,
            how="left",
            left_on="GEOID20",
            right_on=shape_geoid_field,
        )
        shapes_df = shapes_df[["geometry", shape_geoid_field, shape_district_field]]
        assert isinstance(shapes_df, GeoDataFrame)
        del plan_df

        districts_df = shapes_df.dissolve(by=shape_district_field, as_index=False)

        unsorted_shapes: list[dict] = districts_df.to_dict("records")
        sorted_shapes: list[dict] = sorted(
            unsorted_shapes, key=lambda k: k[shape_district_field]
        )
        shapes = [s["geometry"] for s in sorted_shapes]  # discard the id

    ### CALCULATE ANALYTICS ###

    scorecard: dict[str, int | float] = dict()

    # Population deviation

    max_pop: int = max(pop_by_district.values())
    min_pop: int = min(pop_by_district.values())
    target_pop: int = int(total_pop / len(pop_by_district))

    deviation: float = rda.calc_population_deviation(max_pop, min_pop, target_pop)
    scorecard["population_deviation"] = deviation

    # Partisan metrics

    Vf: float = total_d_votes / total_votes
    Vf_array: list[float] = [
        d / tot for d, tot in zip(d_by_district.values(), tot_by_district.values())
    ]

    partisan_metrics: dict = rda.calc_partisan_metrics(Vf, Vf_array)
    bias_metrics: dict = dict()
    bias_metrics["pr_seats"] = partisan_metrics["bias"]["bestS"]
    bias_metrics["pr_pct"] = partisan_metrics["bias"]["bestSf"]
    bias_metrics["estimated_seats"] = partisan_metrics["bias"]["estS"]
    bias_metrics["estimated_seat_pct"] = partisan_metrics["bias"]["estSf"]
    bias_metrics["pr_deviation"] = partisan_metrics["bias"]["deviation"]
    bias_metrics["turnout_bias"] = partisan_metrics["bias"]["tOf"]
    bias_metrics["fptp_seats"] = partisan_metrics["bias"]["fptpS"]
    bias_metrics["seats_bias"] = partisan_metrics["bias"]["bS50"]
    bias_metrics["votes_bias"] = partisan_metrics["bias"]["bV50"]
    bias_metrics["declination"] = partisan_metrics["bias"]["decl"]
    bias_metrics["global_symmetry"] = partisan_metrics["bias"]["gSym"]
    bias_metrics["gamma"] = partisan_metrics["bias"]["gamma"]
    bias_metrics["efficiency_gap"] = partisan_metrics["bias"]["eG"]
    bias_metrics["geometric_seats_bias"] = partisan_metrics["bias"]["bSV"]
    bias_metrics["disproportionality"] = partisan_metrics["bias"]["prop"]
    bias_metrics["mean_median_statewide"] = partisan_metrics["bias"]["mMs"]
    bias_metrics["mean_median_average_district"] = partisan_metrics["bias"]["mMd"]
    bias_metrics["lopsided_outcomes"] = partisan_metrics["bias"]["lO"]
    scorecard.update(bias_metrics)

    responsiveness_metrics: dict = dict()
    responsiveness_metrics["competitive_districts"] = partisan_metrics[
        "responsiveness"
    ]["cD"]
    responsiveness_metrics["competitive_district_pct"] = partisan_metrics[
        "responsiveness"
    ]["cDf"]
    responsiveness_metrics["overall_responsiveness"] = partisan_metrics[
        "responsiveness"
    ][
        "bigR"
    ]  # BIG 'R': Defined in Footnote 22 on P. 10
    responsiveness_metrics["responsiveness"] = partisan_metrics["responsiveness"][
        "littleR"
    ]
    # responsiveness_metrics["minimal_inverse_responsiveness"] = partisan_metrics[
    #     "responsiveness"
    # ][
    #     "mIR"
    # ]  # zeta = (1 / r) - (1 / r_sub_max) : Eq. 5.2.1
    responsiveness_metrics["responsive_districts"] = partisan_metrics["responsiveness"][
        "rD"
    ]
    responsiveness_metrics["responsive_district_pct"] = partisan_metrics[
        "responsiveness"
    ]["rDf"]
    scorecard.update(responsiveness_metrics)

    scorecard.update({"avg_dem_win_pct": partisan_metrics["averageDVf"]})
    scorecard.update({"avg_rep_win_pct": partisan_metrics["averageRVf"]})

    # TODO - Minority

    # Compactness

    if compactness:
        compactness_metrics: dict = rda.calc_compactness(shapes)
        scorecard["reock"] = compactness_metrics["avgReock"]
        scorecard["polsby_popper"] = compactness_metrics["avgPolsby"]
        scorecard["kiwysi"] = compactness_metrics["avgKIWYSI"]

    # Splitting

    splitting_metrics: dict = rda.calc_county_district_splitting(CxD)
    scorecard["county_splitting"] = splitting_metrics["county"]
    scorecard["district_splitting"] = splitting_metrics["district"]
    # NOTE - The simple # of counties split unexpectedly is computed in dra2020/district-analytics,
    # i.e., not in dra2020/dra-analytics in the analytics proper.

    # TODO - Ratings

    return scorecard


### END ###
