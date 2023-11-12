#!/usr/bin/env python3

"""
TEST SAMPLE SCORECARDS
"""

import rdadata as rdd
import rdapy as rda

from rdafn.load import *
from rdafn.analyze import (
    analyze_plan,
    calc_compactness_metrics,
)
from testutils import *


class TestScorecard:
    def test_scorecard(self) -> None:
        for xx in ["NC", "NJ"]:
            plan_path: str = f"sample/{xx}20C_baseline_100.csv"
            plan: list[dict[str, str | int]] = load_plan(plan_path)

            data_project: str = "../rdadata"
            shared_data_dir: str = f"{data_project}/data/"

            data_path: str = rdd.path_to_file([shared_data_dir, xx]) + rdd.file_name(
                [xx, rdd.cycle, "data"], "_", "csv"
            )
            shapes_name: str = f"{xx}_{rdd.cycle}_shapes_simplified.json"
            shapes_path: str = rdd.path_to_file([shared_data_dir, xx]) + shapes_name

            graph_path: str = rdd.path_to_file([shared_data_dir, xx]) + rdd.file_name(
                [xx, rdd.cycle, "graph"], "_", "json"
            )

            ### BOILERPLATE - DON'T CHANGE THIS ###

            data: dict[str, dict[str, int]] = load_data(data_path)
            shapes: dict[str, Any] = load_shapes(shapes_path)
            graph: dict[str, list[str]] = load_graph(graph_path)
            metadata: dict[str, Any] = load_metadata(xx, data_path)

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
