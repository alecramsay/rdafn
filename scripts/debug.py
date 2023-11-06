#!/usr/bin/env python3

"""

DEBUG DISTRICT SHAPE CREATION

To run:

$ scripts/debug.py -s NC

"""

import argparse
from argparse import ArgumentParser, Namespace

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

    verbose: bool = args.verbose

    #

    print("Do something here.")


if __name__ == "__main__":
    main()

### END ###
