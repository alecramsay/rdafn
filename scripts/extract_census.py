#!/usr/bin/env python3
#

"""
Extract census data & normalize it.

For example:

$ scripts/extract_pop.py -s NC

For documentation, type:

$ scripts/extract_census.py -h

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
    """Extract census data & normalize it."""

    args: Namespace = parse_args()

    fips_map: dict[str, str] = STATE_FIPS

    xx: str = args.state
    fips: str = fips_map[xx]

    verbose: bool = args.verbose

    ### READ CONFIG FILE ###

    config_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "config"], "_", "json"
    )
    config: dict[str, Any] = read_json(config_path)

    suffix: str = config["suffix"]
    geoid_field: str = config["geoid"]
    total_field: str = config["total"]
    demo_fields: list[str] = config["demos"]

    ### READ THE CENSUS CSV & EXTRACT THE DATA ###

    census: list[dict] = list()
    fields: list[str] = [
        "TOTAL_VAP",
        "WHITE_VAP",
        "HISPANIC_VAP",
        "BLACK_VAP",
        "NATIVE_VAP",
        "ASIAN_VAP",
        "PACIFIC_VAP",
    ]

    input_path: str = path_to_file([census_dir, xx]) + file_name(
        [cycle, "census", xx + "-" + suffix], "_", "csv"
    )

    with open(FileSpec(input_path).abs_path, "r", encoding="utf-8-sig") as file:
        reader: DictReader[str] = DictReader(
            file, fieldnames=None, restkey=None, restval=None, dialect="excel"
        )

        for row_in in reader:
            row_out: dict = dict()
            row_out["GEOID"] = row_in[geoid_field]
            row_out["TOTAL"] = row_in[total_field]
            for i, field in enumerate(demo_fields):
                row_out[fields[i]] = row_in[demo_fields[i]]

            census.append(row_out)

    ### WRITE THE NORMALIZED CENSUS DATA TO A CSV ###

    output_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "census"], "_", "csv"
    )
    write_csv(output_path, census, ["GEOID", "TOTAL"] + fields)


if __name__ == "__main__":
    main()

### END ###
