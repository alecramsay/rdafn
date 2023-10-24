#!/usr/bin/env python3

"""

TOPOLOGY DEBUGGING

To run:

$ ./topodebug.py

https://pypi.org/project/javascript/

Prerequisites:

npm install -g topojson-client
pip install javascript

"""

import rdapy as rda

from rdafn import *


xx: str = "NC"

#

state_topo: dict[str, Any] = load_topology(xx)

plan_path: str = "data/NC/NC20C_baseline_100.csv"
assignments: list[dict[str, str | int]] = load_plan(plan_path)

#

district_shapes: list = make_district_shapes(state_topo, assignments)

compactness_metrics: dict = rda.calc_compactness(district_shapes)
print(compactness_metrics)

pass

### END ###
