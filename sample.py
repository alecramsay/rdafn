#!/usr/bin/env python3
#
# SAMPLE CODE
#

from rdafn import *

xx: str = "NC"

data: dict[str, dict[str, int]] = load_data(xx)
# shapes: pd.Series | pd.DataFrame | Any = load_shapes(xx)
shapes: pd.Series | pd.DataFrame | Any = None  # TODO

root_path: str = path_to_file([data_dir, xx]) + "NC_2020_Congress_Baseline.csv"
ensemble: list[str] = [root_path]

for plan_path in ensemble:
    plan: Plan = load_plan(plan_path)

    results: dict[str, int | float] = analyze_plan(
        plan.name, plan.assignments, data, shapes
    )

    print(results)

pass
