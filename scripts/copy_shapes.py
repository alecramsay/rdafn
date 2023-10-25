#!/usr/bin/env python3
#

"""
Copy the shapes for a state.

For example:

$ scripts/copy_shapes.py -s NC

For documentation, type:

$ scripts/copy_shapes.py -h

NOTE - Not used. We extract a topology from the shapes instead. See scripts/extract_topo.py.

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
    """Copy the shapes for a state."""

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
