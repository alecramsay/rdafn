#!/usr/bin/env python3

"""
TEST SAMPLE SCORECARDS
"""

import rdadata as rdd
import rdapy as rda

# TODO
# from rdafn.readwrite import read_json
# from rdafn.constants import *
from rdafn.load import *
from rdafn.analyze import (
    analyze_plan,
    calc_compactness_metrics,
)
from testutils import *


class TestScorecard:
    def test_scorecard(self) -> None:
        for xx in ["NC", "NJ"]:
            plan_path: str = f"{rdd.data_dir}/{xx}/{xx}20C_baseline_100.csv"
            plan: list[dict[str, str | int]] = load_plan(plan_path)

            data: dict[str, dict[str, int]] = load_data(xx)
            shapes: dict[str, Any] = load_shapes(xx)
            graph: dict[str, list[str]] = load_graph(xx)
            metadata: dict[str, Any] = load_metadata(xx)

            scorecard: dict[str, Any] = analyze_plan(
                plan, data, shapes, graph, metadata
            )

            #

            expected_path: str = f"{rdd.testdata_dir}/{xx}_DRA_scorecard.json"
            expected: dict[str, Any] = read_json(expected_path)

            decimals_path: str = f"{rdd.testdata_dir}/expected_decimal_places.json"
            approx_floats: dict[str, int] = read_json(decimals_path)
            exact_ints: list[str] = [
                "pr_seats",
                "proportional_opportunities",
                "proportional_coalitions",
            ]
            approx_ints: list[str] = [
                # "kiwysi", # Disabled due to large runtime cost
                "proportionality",
                "competitiveness",
                "minority",
                "compactness",
                "splitting",
            ]

            for metric in exact_ints:
                assert scorecard[metric] == expected[metric]

            for metric in approx_ints:
                assert abs(scorecard[metric] - expected[metric]) <= 1

            for metric in approx_floats:
                assert approx_equal(
                    scorecard[metric], expected[metric], places=approx_floats[metric]
                )

    def test_compactness(self) -> None:
        for xx in ["NC", "NJ"]:
            profile_path = f"testdata/{xx}_root_profile.json"
            profile: dict[str, Any] = read_json(profile_path)
            implicit_district_props: list[dict[str, float]] = profile["shapes"]

            scorecard_path: str = f"{rdd.testdata_dir}/{xx}_DRA_scorecard.json"
            expected: dict[str, Any] = read_json(scorecard_path)

            #

            actual: dict[str, float] = calc_compactness_metrics(implicit_district_props)

            # decimals_path: str = f"{testdata_dir}/expected_decimal_places.json"
            # approx_floats: dict[str, int] = read_json(decimals_path)

            for metric in ["reock", "polsby_popper"]:
                assert approx_equal(actual[metric], expected[metric], places=4)


### END ###
