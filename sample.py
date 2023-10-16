#!/usr/bin/env python3
#
# SAMPLE CODE
#

from rdafn import *

xx: str = "NC"

data: dict[str, dict[str, int]] = load_data(xx)
# shapes: pd.Series | pd.DataFrame | Any = load_shapes(xx)
shapes: pd.Series | pd.DataFrame | Any = None  # TODO

root_plan: str = path_to_file([data_dir, xx]) + "NC20C_baseline_100.csv"
ensemble: list[str] = [root_plan]

for plan_path in ensemble:
    plan: Plan = load_plan(plan_path)

    scorecard: dict[str, int | float] = analyze_plan(
        plan.name, plan.assignments, data, shapes
    )

    print()
    print(f"Scorecard for plan {plan.name}:")
    for metric in scorecard:
        print(f"{metric}: {scorecard[metric]}")
    print()

pass
