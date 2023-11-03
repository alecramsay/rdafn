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

from rdafn import *


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
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def main() -> None:
    """Abstract the precinct shapes for a state.

    * Load the state's graph w/ OUT_OF_STATE neighbors.
    * For each shape:
      - Calculate the area
      - Calculate the shared borders by neighbor
      - Extract the exterior coordinates

    """

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### COPY THE SHAPES ###

    shapes_file: str = f"tl_2020_{fips}_vtd20"
    input_path: str = path_to_file([f"../../{shapes_dir}", xx, shapes_file])

    working_dir: str = f"{data_dir}/{xx}"

    os.chdir(working_dir)
    commands: list[str] = [
        f"cp -R {input_path} {shapes_file}/",
        f"zip -r {shapes_file}.zip {shapes_file}/",
        f"rm -rf {shapes_file}/",
    ]
    for command in commands:
        # print(command)
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
