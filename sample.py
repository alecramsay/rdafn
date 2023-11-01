#!/usr/bin/env python3

"""
SAMPLE CODE

To run:

$ ./sample.py
"""

import os

from rdafn import *

# Specify a state and an ensemble of plans

xx: str = "NC"

ensemble: list[str] = [
    os.path.expanduser(f"{data_dir}/{xx}/") + x
    for x in [
        f"{xx}20C_baseline_100.csv",
        # "NC20C_I000K01N14_vtd_assignments.csv",
        # "NC20C_I001K01N14_vtd_assignments.csv",
        # "NC20C_I002K01N14_vtd_assignments.csv",
        # "NC20C_I003K01N14_vtd_assignments.csv",
        # "NC20C_I004K01N14_vtd_assignments.csv",
    ]
]

# Load the state
# This is boilerplate: nothing needs to change here.

data: dict[str, dict[str, int]] = load_data(xx)
state_topo: dict[str, Any] = load_topology(xx)
D: int = DISTRICTS_BY_STATE[xx]["congress"]
C: int = COUNTIES_BY_STATE[xx]

sample: list[dict[str, str | int]] = load_plan(ensemble[0])
county_to_index, district_to_index = index_counties_and_districts(sample)

# Analyze each plan in the ensemble
# The looping and analytics call are boilerplate.
# You just need to do something with the resulting "scorecard".

for plan_path in ensemble:
    assignments: list[dict[str, str | int]] = load_plan(plan_path)

    scorecard: dict[str, Any] = analyze_plan(
        assignments,
        data,
        state_topo,
        D,
        C,
        county_to_index,
        district_to_index,
    )

    # Do something with the resulting "scorecard"

    print()
    print(f"Scorecard:")
    for metric in scorecard:
        print(f"{metric}: {scorecard[metric]}")
    print()

pass
