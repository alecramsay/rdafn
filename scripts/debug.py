#!/usr/bin/env python3

"""

DEBUG DISTRICT SHAPE CREATION

To run:

$ scripts/debug.py -s NC

"""

import argparse
from argparse import ArgumentParser, Namespace

# from shapely.geometry import (
#     shape,
#     Polygon,
#     MultiPolygon,
# )

# import rdapy as rda
from rdafn import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(description="Debug")

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Debug"""

    args: Namespace = parse_args()

    xx: str = args.state
    xx = "NJ"  # HACK

    verbose: bool = args.verbose

    #

    plan_path: str = os.path.expanduser(
        f"{data_dir}/{xx}/" + f"{xx}20C_baseline_100.csv"
    )
    plan: list[dict[str, int]] = load_plan(plan_path)

    topo: dict[str, Any] = load_topology(xx)
    D: int = DISTRICTS_BY_STATE[xx]["congress"]

    #

    district_geojsons: list[dict[str, Any]] = merge_features(topo, plan)

    for i, d in enumerate(district_geojsons):
        output_path: str = os.path.expanduser(
            f"~/Downloads/{xx}/" + f"{xx}_district_{i+1}.geojson"
        )
        write_json(output_path, d)


if __name__ == "__main__":
    main()

### END ###
