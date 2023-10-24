#!/usr/bin/env python3
#
# SAMPLE CODE
#

from rdafn import *

xx: str = "NC"
N: int = 14  # TODO - Get this from metadata
C: int = 100  # TODO - Ditto

#

data: dict[str, dict[str, int]] = load_data(xx)
state_topo: dict[str, Any] = load_topology(xx)

root_plan: str = path_to_file([data_dir, xx]) + "NC20C_baseline_100.csv"
ensemble: list[str] = [root_plan]

for plan_path in ensemble:
    assignments: list[dict[str, str | int]] = load_plan(plan_path)

    scorecard: dict[str, Any] = analyze_plan(assignments, data, state_topo, N, C)

    print()
    print(f"Scorecard:")
    for metric in scorecard:
        print(f"{metric}: {scorecard[metric]}")
    print()

pass
