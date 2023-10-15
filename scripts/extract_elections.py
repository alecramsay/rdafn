#!/usr/bin/env python3
#

"""
Extract election data & normalize it.

For example:

$ scripts/extract_elections.py -s NC

For documentation, type:

$ scripts/extract_elections.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdafn import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Extract election data from a vtd_data CSV file."
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
    """Extract election data & normalize it."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    ### READ CONFIG FILE ###

    config_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "config"], "_", "json"
    )
    config: dict[str, Any] = read_json(config_path)

    suffix: str = config["election_suffix"]
    geoid_field: str = config["geoid"]
    elections: list[str] = config["elections"]

    if suffix != "":
        suffix = "-" + suffix

    ### READ THE ELECTIONS CSV & EXTRACT THE DATA ###

    election: list[dict] = list()
    total_fields: list[str] = [f"Tot_{e}" for e in elections]
    rep_fields: list[str] = [f"R_{e}" for e in elections]
    dem_fields: list[str] = [f"D_{e}" for e in elections]

    input_path: str = path_to_file([census_dir, xx]) + file_name(
        [cycle, "election", xx + suffix], "_", "csv"
    )

    with open(FileSpec(input_path).abs_path, "r", encoding="utf-8-sig") as file:
        reader: DictReader[str] = DictReader(
            file, fieldnames=None, restkey=None, restval=None, dialect="excel"
        )

        for row_in in reader:
            row_out: dict = dict()
            row_out["GEOID"] = row_in[geoid_field]
            row_out["TOT"] = sum([int(row_in[x]) for x in total_fields])
            row_out["REP"] = sum([int(row_in[x]) for x in rep_fields])
            row_out["DEM"] = sum([int(row_in[x]) for x in dem_fields])
            row_out["OTH"] = row_out["TOT"] - row_out["REP"] - row_out["DEM"]

            election.append(row_out)

    ### WRITE THE NORMALIZED CENSUS DATA TO A CSV ###

    output_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "election"], "_", "csv"
    )
    write_csv(output_path, election, ["GEOID", "TOT", "REP", "DEM", "OTH"])


if __name__ == "__main__":
    main()

### END ###
