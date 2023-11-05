#!/usr/bin/env python3
#

"""
Extract the topology for a state.

For example:

$ scripts/extract_topo.py -s NC

For documentation, type:

$ scripts/extract_topo.py -h

References:

https://medium.com/@terrycrowley/small-pleasures-of-programming-ae4f50dde67a
https://medium.com/p/388e1ace26f0

https://github.com/topojson/topojson <<< Deprecated
https://github.com/topojson/topojson-server
https://github.com/topojson/topojson-client
https://github.com/topojson/topojson-simplify

https://medium.com/@mbostock/command-line-cartography-part-1-897aa8f8ca2c
https://medium.com/@mbostock/command-line-cartography-part-3-1158e4c55a1e

https://www.npmjs.com/package/topojson <<< Deprecated
https://www.npmjs.com/package/topojson-server
https://www.npmjs.com/package/topojson-client
https://www.npmjs.com/package/topojson-simplify

Prerequisites:

npm install -g shapefile
npm install -g ndjson-cli
npm install -g topojson <<< Deprecated
npm install -g topojson-server
npm install -g topojson-client
npm install -g topojson-simplify

npm list -g --depth=0

"""

import os
from pathlib import Path
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
    """Extract the topolgy for a state."""

    args: Namespace = parse_args()

    xx: str = args.state

    verbose: bool = args.verbose

    #

    fips_map: dict[str, str] = STATE_FIPS
    fips: str = fips_map[xx]

    ### EXTRACT THE TOPLOGY ###

    shapes_file: str = f"tl_2020_{fips}_vtd20"
    shapes_path: str = FileSpec(
        path_to_file([f"{shapes_dir}", xx, shapes_file])
    ).abs_path

    temp_dir: str = FileSpec(path_to_file(["temp"])).abs_path
    output_dir: str = FileSpec(path_to_file([data_dir, xx])).abs_path

    commands: list[str] = [
        f"shp2json {shapes_path}/{shapes_file}.shp -o {temp_dir}/{xx}_vtd.json",
        f"ndjson-split 'd.features' < {temp_dir}/{xx}_vtd.json > {temp_dir}/{xx}_vtd.ndjson",
        f"geo2topo -n collection={temp_dir}/{xx}_vtd.ndjson > {output_dir}/{xx}_vtd_topo.json",
        f"toposimplify -s 1E-10 -f < {output_dir}/{xx}_vtd_topo.json > {output_dir}/{xx}_vtd_simple_topo.json",
        # f"toposimplify -p 1 -f < {output_dir}/{xx}_vtd_topo.json > {output_dir}/{xx}_vtd_simple_topo.json",
        f"topoquantize 1e5 < {output_dir}/{xx}_vtd_simple_topo.json > {output_dir}/{xx}_vtd_quantized_topo.json",
    ]
    for command in commands:
        # print(command)
        os.system(command)


if __name__ == "__main__":
    main()

### END ###