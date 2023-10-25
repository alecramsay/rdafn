#!/usr/bin/env python3

"""
SAMPLE CODE

To run:

$ ./sample.py
"""

from rdafn import *

# Specify a state and an ensemble of plans

xx: str = "NC"
root_plan: str = path_to_file([data_dir, xx]) + "NC20C_baseline_100.csv"
ensemble: list[str] = [root_plan]

# Load the state

data: dict[str, dict[str, int]] = load_data(xx)
state_topo: dict[str, Any] = load_topology(xx)
N: int = DISTRICTS_BY_STATE[xx]["congress"]
C: int = COUNTIES_BY_STATE[xx]

# Analyze each plan in the ensemble

for plan_path in ensemble:
    assignments: list[dict[str, str | int]] = load_plan(plan_path)

    scorecard: dict[str, Any] = analyze_plan(assignments, data, state_topo, N, C)

    # Do something with the resulting "scorecard"

    print()
    print(f"Scorecard:")
    for metric in scorecard:
        print(f"{metric}: {scorecard[metric]}")
    print()

pass
