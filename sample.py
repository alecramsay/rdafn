#!/usr/bin/env python3
#
# SAMPLE CODE
#

from rdafn import *

xx: str = "NC"
plan_path: str = path_to_file([data_dir, xx]) + "NC_2020_Congress_Baseline.csv"

data: dict[str, dict[str, int]] = load_data(xx)
# shapes: dict[str, dict[str, int]] = load_shapes(xx)

plan: list[dict[str, int]] = load_plan(plan_path)

pass
