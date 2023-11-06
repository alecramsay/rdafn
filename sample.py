#!/usr/bin/env python3

"""
SAMPLE CODE

To run:

$ ./sample.py

"""

import os

from rdafn import *

# Specify a state and an ensemble of plans

xx: str = "NJ"

ensemble: list[str] = [
    os.path.expanduser(f"{data_dir}/{xx}/") + x
    for x in [
        f"{xx}20C_baseline_100.csv",
        # More plans here ...
    ]
]

# Load the state -- This is boilerplate: nothing needs to change.

data: dict[str, dict[str, int]] = load_data(xx)
shapes: dict[str, Any] = load_shapes(xx)
graph: dict[str, list[str]] = load_graph(xx)
metadata: dict[str, Any] = load_metadata(xx)

#

# Analyze each plan in an ensemble

for plan_path in ensemble:
    try:
        # Get a plan from the ensemble

        assignments: list[dict[str, str | int]] = load_plan(plan_path)

        # Score it

        scorecard: dict[str, Any] = analyze_plan(
            assignments,
            data,
            shapes,
            graph,
            metadata,
        )

        # Do something with the resulting "scorecard"

        print()
        print(f"Scorecard:")
        for metric in scorecard:
            print(f"{metric}: {scorecard[metric]}")
        print()

    except Exception as e:
        print(f"Error analyzing {plan_path}: {e}")

### END ###
