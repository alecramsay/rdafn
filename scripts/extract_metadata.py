#!/usr/bin/env python3
#

"""
Extract metadata for a state.

For example:

$ scripts/extract_metadata.py -s NC

For documentation, type:

$ scripts/extract_metadata.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdafn import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract census data from a vtd_data CSV file."
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
    """Extract metadata for a state."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### INFER COUNTY FIPS CODES ###

    census_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "census"], "_", "csv"
    )
    census: list = read_csv(census_path, [str] + [int] * 9)

    counties: set[str] = set()
    for row in census:
        precinct: str = str(row["GEOID"] if "GEOID" in row else row["GEOID20"])
        county: str = GeoID(precinct).county[2:]
        counties.add(county)

    ### GATHER METADATA ###

    C: int = COUNTIES_BY_STATE[xx]
    D: int = DISTRICTS_BY_STATE[xx]["congress"]

    county_to_index: dict[str, int] = {county: i for i, county in enumerate(counties)}

    district_to_index: dict[int, int] = {
        district: i for i, district in enumerate(range(1, D + 1))
    }  # NOTE - This is getting persisted as JSON, so districts will be strings

    metadata: dict[str, Any] = dict()
    metadata["C"] = C
    metadata["D"] = D
    metadata["county_to_index"] = county_to_index
    metadata["district_to_index"] = district_to_index

    ### PICKLE THE METADATA ###

    output_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "metadata"], "_", "pickle"
    )
    write_pickle(output_path, metadata)


if __name__ == "__main__":
    main()

### END ###
