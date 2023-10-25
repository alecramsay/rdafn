#!/usr/bin/env python3

"""
ANALYZE A PLAN
"""

from collections import defaultdict

import rdapy as rda

from .constants import *
from .utils import *
from .districtshapes import make_district_shapes

### FIELD NAMES ###

total_pop_field: str = census_fields[0]
total_vap_field: str = census_fields[1]
# white_vap_field: str = census_fields[2]
# hispanic_vap_field: str = census_fields[3]
# black_vap_field: str = census_fields[4]
# native_vap_field: str = census_fields[5]
# asian_vap_field: str = census_fields[6]
# pacific_vap_field: str = census_fields[7]
# minority_vap_field: str = census_fields[8]

# total_votes_field: str = election_fields[0]
rep_votes_field: str = election_fields[1]
dem_votes_field: str = election_fields[2]
# oth_votes_field: str = election_fields[3]


@time_function
def analyze_plan(
    assignments: list[dict[str, str | int]],
    data: dict[str, dict[str, int]],
    topo: dict[str, Any],
    n_districts: int,
    n_counties: int,
    county_to_index: dict[str, int],
    district_to_index: dict[int, int],
) -> dict[str, Any]:
    """Analyze a plan."""

    ### AGGREGATE DATA & SHAPES BY DISTRICT ###

    aggregates: dict[str, Any] = aggregate_data_by_district(
        assignments, data, n_districts, n_counties, county_to_index, district_to_index
    )
    district_shapes: list = make_district_shapes(topo, assignments)

    ### CALCULATE THE METRICS ###

    deviation: float = calc_population_deviation(
        aggregates["pop_by_district"], aggregates["total_pop"], n_districts
    )
    partisan_metrics: dict[str, float] = calc_partisan_metrics(
        aggregates["total_d_votes"],
        aggregates["total_votes"],
        aggregates["d_by_district"],
        aggregates["tot_by_district"],
    )
    minority_metrics: dict[str, float] = calc_minority_metrics(
        aggregates["demos_totals"], aggregates["demos_by_district"], n_districts
    )
    compactness_metrics: dict[str, float] = calc_compactness_metrics(district_shapes)
    splitting_metrics: dict[str, float] = calc_splitting_metrics(aggregates["CxD"])

    scorecard: dict[str, Any] = dict()
    scorecard["population_deviation"] = deviation
    scorecard.update(partisan_metrics)
    scorecard.update(minority_metrics)
    scorecard.update(compactness_metrics)
    scorecard.update(splitting_metrics)

    ### RATE THE DIMENSIONS ###

    ratings: dict[str, int] = rate_dimensions(
        proportionality=(
            scorecard["disproportionality"],
            scorecard["estimated_vote_pct"],
            scorecard["estimated_seat_pct"],
        ),
        competitiveness=(scorecard["competitive_district_pct"],),
        minority=(
            scorecard["opportunity_districts"],
            scorecard["proportional_opportunities"],
            scorecard["coalition_districts"],
            scorecard["proportional_coalitions"],
        ),
        compactness=(scorecard["reock"], scorecard["polsby_popper"]),
        splitting=(
            scorecard["county_splitting"],
            scorecard["district_splitting"],
            n_counties,
            n_districts,
        ),
    )
    scorecard.update(ratings)

    return scorecard


### HELPER FUNCTIONS ###


def index_counties_and_districts(assignments: list[dict[str, str | int]]) -> tuple:
    """Index counties and districts.

    NOTE - This only needs to be done once per batch of plans being analyzed for a state.
    """

    counties: set[str] = set()
    districts: set[int] = set()

    for row in assignments:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        district: int = int(row["DISTRICT"] if "DISTRICT" in row else row["District"])

        county: str = GeoID(precinct).county[2:]

        counties.add(county)
        districts.add(district)

    county_to_index: dict[str, int] = {county: i for i, county in enumerate(counties)}
    district_to_index: dict[int, int] = {
        district: i for i, district in enumerate(districts)
    }

    return county_to_index, district_to_index


def aggregate_data_by_district(
    assignments: list[dict[str, str | int]],
    data: dict[str, dict[str, int]],
    n_districts: int,
    n_counties: int,
    county_to_index: dict[str, int],
    district_to_index: dict[int, int],
) -> dict[str, Any]:
    """Aggregate census & election data by district."""

    total_pop: int = 0
    pop_by_district: defaultdict[int, int] = defaultdict(int)

    total_votes: int = 0
    total_d_votes: int = 0
    d_by_district: dict[int, int] = defaultdict(int)
    tot_by_district: dict[int, int] = defaultdict(int)
    # d_by_district: defaultdict[int, int] = defaultdict(int)
    # tot_by_district: defaultdict[int, int] = defaultdict(int)

    demos_totals: dict[str, int] = defaultdict(int)
    demos_by_district: list[dict[str, int]] = [
        defaultdict(int) for _ in range(n_districts + 1)
    ]

    CxD: list[list[float]] = [[0.0] * n_counties for _ in range(n_districts)]

    for row in assignments:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        district: int = int(row["DISTRICT"] if "DISTRICT" in row else row["District"])

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

        for demo in census_fields[1:]:  # Everything except total population
            demos_totals[demo] += data[precinct][demo]
            demos_by_district[district][demo] += data[precinct][demo]

        # For county-district splitting

        county: str = GeoID(precinct).county[2:]

        i: int = district_to_index[district]
        j: int = county_to_index[county]

        CxD[i][j] += pop

    aggregates: dict[str, Any] = {
        "total_pop": total_pop,
        "pop_by_district": pop_by_district,
        "total_votes": total_votes,
        "total_d_votes": total_d_votes,
        "d_by_district": d_by_district,
        "tot_by_district": tot_by_district,
        "demos_totals": demos_totals,
        "demos_by_district": demos_by_district,
        "CxD": CxD,
    }

    return aggregates


def calc_population_deviation(
    pop_by_district: defaultdict[int, int], total_pop: int, n_districts: int
) -> float:
    """Calculate population deviation."""

    max_pop: int = max(pop_by_district.values())
    min_pop: int = min(pop_by_district.values())
    target_pop: int = int(total_pop / n_districts)

    deviation: float = rda.calc_population_deviation(max_pop, min_pop, target_pop)

    return deviation


def calc_partisan_metrics(
    total_d_votes: int,
    total_votes: int,
    d_by_district: dict[int, int],
    tot_by_district: dict[int, int],
) -> dict[str, float]:
    """Calulate partisan metrics."""

    partisan_metrics: dict[str, float] = dict()

    Vf: float = total_d_votes / total_votes
    Vf_array: list[float] = [
        d / tot for d, tot in zip(d_by_district.values(), tot_by_district.values())
    ]
    partisan_metrics["estimated_vote_pct"] = Vf

    all_results: dict = rda.calc_partisan_metrics(Vf, Vf_array)

    partisan_metrics["pr_deviation"] = all_results["bias"]["deviation"]
    partisan_metrics["pr_seats"] = all_results["bias"]["bestS"]
    partisan_metrics["pr_pct"] = all_results["bias"]["bestSf"]
    partisan_metrics["estimated_seats"] = all_results["bias"]["estS"]
    partisan_metrics["estimated_seat_pct"] = all_results["bias"]["estSf"]
    partisan_metrics["fptp_seats"] = all_results["bias"]["fptpS"]

    partisan_metrics["disproportionality"] = all_results["bias"]["prop"]
    partisan_metrics["efficiency_gap"] = all_results["bias"]["eG"]
    partisan_metrics["gamma"] = all_results["bias"]["gamma"]

    partisan_metrics["seats_bias"] = all_results["bias"]["bS50"]
    partisan_metrics["votes_bias"] = all_results["bias"]["bV50"]
    partisan_metrics["geometric_seats_bias"] = all_results["bias"]["bSV"]
    partisan_metrics["global_symmetry"] = all_results["bias"]["gSym"]

    partisan_metrics["declination"] = all_results["bias"]["decl"]
    partisan_metrics["mean_median_statewide"] = all_results["bias"]["mMs"]
    partisan_metrics["mean_median_average_district"] = all_results["bias"]["mMd"]
    partisan_metrics["turnout_bias"] = all_results["bias"]["tOf"]
    partisan_metrics["lopsided_outcomes"] = all_results["bias"]["lO"]

    partisan_metrics["competitive_districts"] = all_results["responsiveness"]["cD"]
    partisan_metrics["competitive_district_pct"] = all_results["responsiveness"]["cDf"]

    partisan_metrics["responsiveness"] = all_results["responsiveness"]["littleR"]
    partisan_metrics["responsive_districts"] = all_results["responsiveness"]["rD"]
    partisan_metrics["responsive_district_pct"] = all_results["responsiveness"]["rDf"]
    partisan_metrics["overall_responsiveness"] = all_results["responsiveness"][
        "bigR"
    ]  # BIG 'R': Defined in Footnote 22 on P. 10
    # partisan_metrics["minimal_inverse_responsiveness"] = all_results[
    #     "responsiveness"
    # ][
    #     "mIR"
    # ]  # zeta = (1 / r) - (1 / r_sub_max) : Eq. 5.2.1

    partisan_metrics["avg_dem_win_pct"] = all_results["averageDVf"]
    partisan_metrics["avg_rep_win_pct"] = (
        1.0 - all_results["averageRVf"]
    )  # Invert the D % to get the R %.

    return partisan_metrics


def calc_minority_metrics(
    demos_totals: dict[str, int],
    demos_by_district: list[dict[str, int]],
    n_districts: int,
) -> dict[str, float]:
    """Calculate minority metrics."""

    statewide_demos: dict[str, float] = dict()
    for demo in census_fields[2:]:  # Skip total population & total VAP
        simple_demo: str = demo.split("_")[0].lower()
        statewide_demos[simple_demo] = (
            demos_totals[demo] / demos_totals[total_vap_field]
        )

    by_district: list[dict[str, float]] = list()
    for i in range(1, n_districts + 1):
        district_demos: dict[str, float] = dict()
        for demo in census_fields[2:]:  # Skip total population & total VAP
            simple_demo: str = demo.split("_")[0].lower()
            district_demos[simple_demo] = (
                demos_by_district[i][demo] / demos_by_district[i][total_vap_field]
            )

        by_district.append(district_demos)

    minority_metrics: dict[str, float] = rda.calc_minority_opportunity(
        statewide_demos, by_district
    )

    return minority_metrics


def calc_compactness_metrics(district_shapes: list) -> dict[str, float]:
    """Calculate compactness metrics."""

    all_results: dict[str, float] = rda.calc_compactness(district_shapes)

    compactness_metrics: dict[str, float] = dict()
    compactness_metrics["reock"] = all_results["avgReock"]
    compactness_metrics["polsby_popper"] = all_results["avgPolsby"]
    # Invert the KIWYSI rank (1-100, lower is better) to a score (0-100, higher is better)
    compactness_metrics["kiwysi"] = 100 - round(all_results["avgKIWYSI"]) + 1

    return compactness_metrics


def calc_splitting_metrics(CxD: list[list[float]]) -> dict[str, float]:
    """Calculate county-district splitting metrics."""

    all_results: dict[str, float] = rda.calc_county_district_splitting(CxD)

    splitting_metrics: dict[str, float] = dict()
    splitting_metrics["county_splitting"] = all_results["county"]
    splitting_metrics["district_splitting"] = all_results["district"]

    # NOTE - The simple # of counties split unexpectedly is computed in dra2020/district-analytics,
    # i.e., not in dra2020/dra-analytics in the analytics proper.

    return splitting_metrics


def rate_dimensions(
    *,
    proportionality: tuple,
    competitiveness: tuple,
    minority: tuple,
    compactness: tuple,
    splitting: tuple,
) -> dict[str, int]:
    """Rate the dimensions of a plan."""

    ratings: dict[str, int] = dict()

    disproportionality, Vf, Sf = proportionality
    ratings["proportionality"] = rda.rate_proportionality(disproportionality, Vf, Sf)

    cdf = competitiveness[0]
    ratings["competitiveness"] = rda.rate_competitiveness(cdf)

    od, pod, cd, pcd = minority
    ratings["minority"] = rda.rate_minority_opportunity(od, pod, cd, pcd)

    avg_reock, avg_polsby = compactness
    reock_rating: int = rda.rate_reock(avg_reock)
    polsby_rating: int = rda.rate_polsby(avg_polsby)
    ratings["compactness"] = rda.rate_compactness(reock_rating, polsby_rating)

    county_splitting, district_splitting, n_counties, n_districts = splitting
    county_rating: int = rda.rate_county_splitting(
        county_splitting, n_counties, n_districts
    )
    district_rating: int = rda.rate_district_splitting(
        district_splitting, n_counties, n_districts
    )
    ratings["splitting"] = rda.rate_splitting(county_rating, district_rating)

    return ratings


### END ###
