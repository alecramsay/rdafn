#!/usr/bin/env python3

"""

DEBUG DISTRICT SHAPE CREATION

To run:

$ scripts/debug.py -s NC

"""

import argparse
from argparse import ArgumentParser, Namespace

from shapely.geometry import (
    shape,
    Polygon,
    MultiPolygon,
    # Point,
    # MultiPoint,
    # LineString,
    # MultiLineString,
    # LinearRing,
    # GeometryCollection,
)

import rdapy as rda
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

    plan_path: str = os.path.expanduser(f"{data_dir}/{xx}/") + f"{xx}20C_baseline_100.csv")
    plan: list[dict[str, str | int]] = load_plan(plan_path)

    state_topo: dict[str, Any] = load_topology(xx)
    D: int = DISTRICTS_BY_STATE[xx]["congress"]

    #

    shapes_path = "testdata/compactness/NC-116th-Congressional.geojson"
    geojson = read_json(shapes_path)

    expected_path = "testdata/compactness/NC-116th-Congressional.json"
    expected = read_json(expected_path)

    district_shapes: list[
        Polygon
        | MultiPolygon
        # | Point
        # | MultiPoint
        # | LineString
        # | MultiLineString
        # | LinearRing
        # | GeometryCollection
    ] = list()

    for f in geojson["features"]:
        shp: Polygon | MultiPolygon = geojson_to_shape(f["geometry"])

        district_shapes.append(shp)

    actual: dict = rda.calc_compactness(district_shapes)
    x = actual["byDistrict"]

    n_districts: int = len(actual["byDistrict"])

    #

    for k, v in actual.items():
        print(f"{k}: {v}")

    pass


if __name__ == "__main__":
    main()

### END ###
