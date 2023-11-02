#!/usr/bin/env python3

"""
TEST SAMPLE SCORECARDS
"""

import rdapy as rda

from rdafn.readwrite import read_json
from rdafn.constants import *
from rdafn.load import *
from rdafn.analyze import analyze_plan, index_counties_and_districts
from testutils import *


class TestScorecard:
    def test_scorecard(self) -> None:
        for xx in ["NC", "NJ"]:
            plan_path: str = f"{data_dir}/{xx}/{xx}20C_baseline_100.csv"

            data: dict[str, dict[str, int]] = load_data(xx)
            state_topo: dict[str, Any] = load_topology(xx)
            D: int = DISTRICTS_BY_STATE[xx]["congress"]
            C: int = COUNTIES_BY_STATE[xx]

            sample: list[dict[str, str | int]] = load_plan(plan_path)
            county_to_index, district_to_index = index_counties_and_districts(sample)

            assignments: list[dict[str, str | int]] = sample

            scorecard: dict[str, Any] = analyze_plan(
                assignments,
                data,
                state_topo,
                D,
                C,
                county_to_index,
                district_to_index,
            )

            #

            expected_path: str = f"{testdata_dir}/{xx}_DRA_scorecard.json"
            expected: dict[str, Any] = read_json(expected_path)

            decimals_path: str = f"{testdata_dir}/expected_decimal_places.json"
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


### END ###
