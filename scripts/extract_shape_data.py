#!/usr/bin/env python3
#

"""
Abstract precinct shapes so the area, perimeter, and diameter of district shapes
can be computed *implicitly*.

For example:

$ scripts/extract_shape_data.py -s NC

For documentation, type:

$ scripts/extract_shape_data.py -h

"""

import os
import argparse
from argparse import ArgumentParser, Namespace

from shapely.geometry import Polygon, MultiPolygon

from rdafn import *

EPSILON: float = 1.0e-12
THRESHOLD: float = 0.000255
# THRESHOLD: float = 0.00026 # too high
# THRESHOLD: float = 0.00025  # too low


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Copy the shapes for a state."
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NC",
        help="The two-character state code (e.g., NC)",
        type=str,
    )
    parser.add_argument(
        "-u",
        "--unsimplified",
        dest="unsimplified",
        action="store_true",
        help="Simplify mode",
    )

    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Abstract the precinct shapes for a state."""

    args: Namespace = parse_args()

    xx: str = args.state
    simplify: bool = not args.unsimplified

    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### LOAD THE GRAPH ###

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "graph"], "_", "json"
    )

    graph: dict[str, list[str]] = read_json(graph_path)

    ### LOAD THE SHAPES ###

    vtd_path: str = path_to_file([shapes_dir, xx]) + file_name(
        ["tl_2020", fips, "vtd20"], "_"
    )
    vtd_shps: dict
    other: Optional[dict[str, Any]]
    vtd_shps, other = read_shapes(vtd_path, "GEOID20")

    ### ABSTRACT THE SHAPES ###

    vtd_abstracts: dict[str, dict[str, Any]] = dict()

    for item in vtd_shps.items():
        geoid: str = item[0]
        shp: Polygon | MultiPolygon = item[1]

        if simplify:
            shp = shp.simplify(THRESHOLD, preserve_topology=True)

        area: float = shp.area

        arcs: dict[str, float] = dict()  # The shared border lengths by neighbor
        neighbors: list[str] = graph[geoid]
        perimeter: float = shp.length
        total_shared_border: float = 0.0

        for neighbor in neighbors:
            if neighbor == OUT_OF_STATE:
                continue
            neighbor_shp: Polygon | MultiPolygon = vtd_shps[neighbor]
            shared_edge = shp.intersection(neighbor_shp)
            shared_border: float = shared_edge.length

            arcs[neighbor] = shared_border
            total_shared_border += shared_border

        remaining: float = perimeter - total_shared_border
        if remaining > EPSILON:
            arcs[OUT_OF_STATE] = remaining

        ch = shp.convex_hull
        pts: list[tuple[float, float]] = list(ch.exterior.coords)

        vtd_abstracts[geoid] = {
            "area": area,
            "arcs": arcs,
            "exterior": pts,
        }

    ### PICKLE THE DATA ###

    pickle_name: str = (
        f"{xx}_{cycle}_shapes_simplified.pickle"
        if simplify
        else f"{xx}_{cycle}_shapes.pickle"
    )
    output_path: str = path_to_file([data_dir, xx]) + pickle_name
    write_pickle(output_path, vtd_abstracts)


if __name__ == "__main__":
    main()

### END ###
