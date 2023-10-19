#!/usr/bin/env python3
#
# SAMPLE CODE
#

from rdafn import *

xx: str = "NC"
N: int = 14  # TODO - Get this from metadata
C: int = 100  # TODO - Ditto

compactness: bool = False

#

data: dict[str, dict[str, int]] = load_data(xx)
shapes: pd.Series | pd.DataFrame | Any = None
if compactness:
    shapes = load_shapes(xx)

root_plan: str = path_to_file([data_dir, xx]) + "NC20C_baseline_100.csv"
ensemble: list[str] = [root_plan]

for plan_path in ensemble:
    plan: Plan = load_plan(plan_path)

    scorecard: dict[str, Any] = analyze_plan(
        plan.name, plan.assignments, data, shapes, N, C, compactness
    )

    print()
    print(f"Scorecard for plan {plan.name}:")
    for metric in scorecard:
        print(f"{metric}: {scorecard[metric]}")
    print()

pass
