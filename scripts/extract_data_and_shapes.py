#!/usr/bin/env python3
#

"""
Extract the census & election data for a state.

For example:

$ scripts/extract_data_and_shapes.py -s NC

For documentation, type:

$ scripts/extract_data_and_shapes.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdafn import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract the census & election data for a state."
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
    """Extract the census & election data for a state."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### RUN THE SCRIPTS ###

    commands: list[str] = [
        "scripts/extract_census.py -s {xx}",
        "scripts/extract_elections.py -s {xx}",
        "scripts/join_data.py -s {xx}",
        "scripts/extract_topo.py -s {xx}",
        # "scripts/copy_shapes.py -s {xx}",
    ]

    for command in commands:
        command = command.format(xx=xx)
        print(f"> {command} ...")
        os.system(command)


if __name__ == "__main__":
    main()

### END ###
