#!/usr/bin/env python3

"""

SAMPLE SCRIPT FOR ANALYZING AN ENSEMBLE OF PLANS

To run:

$ scripts/analyze_plan.py -s NJ

For documentation, type:

$ scripts/analyze_plan.py -h

"""

import argparse
from argparse import ArgumentParser, Namespace

from rdafn import *


def parse_args() -> Namespace:
    parser: ArgumentParser = argparse.ArgumentParser(
        description="Analyze an ensemble of plans"
    )

    parser.add_argument(
        "-s",
        "--state",
        default="NJ",
        help="The two-character state code (e.g., NJ)",
        type=str,
    )
    parser.add_argument(
        "-e",
        "--ensemble",
        default="~/Downloads/",  # TODO: Change this a default ensemble
        help="Path to ensemble file",
        type=str,
    )
    parser.add_argument(
        "-v", "--verbose", dest="verbose", action="store_true", help="Verbose mode"
    )

    args: Namespace = parser.parse_args()
    return args


def plans_from_ensemble(
    xx: str, ensemble_path: str
) -> Generator[list[dict[str, str | int]], None, None]:
    """Return plans (assignments) one at a time from an ensemble file"""

    # Replace this with code that reads an ensemble file and returns plans one at a time
    ensemble: list[list[dict[str, str | int]]] = [
        load_plan(os.path.expanduser(f"{data_dir}/{xx}/") + f"{xx}20C_baseline_100.csv")
    ]

    for plan in ensemble:
        yield plan


def main() -> None:
    """Analyze an ensemble of plans"""

    args: Namespace = parse_args()

    xx: str = args.state
    ensemble_path: str = args.ensemble

    verbose: bool = args.verbose

    # Load the state -- This is boilerplate: nothing needs to change.

    data: dict[str, dict[str, int]] = load_data(xx)
    shapes: dict[str, Any] = load_shapes(xx)
    graph: dict[str, list[str]] = load_graph(xx)
    metadata: dict[str, Any] = load_metadata(xx)

    # Analyze each plan in an ensemble

    for assignments in plans_from_ensemble(xx, ensemble_path):
        try:
            scorecard: dict[str, Any] = analyze_plan(
                assignments,
                data,
                shapes,
                graph,
                metadata,
            )

            # TODO - Do something with the resulting "scorecard"

            print(scorecard)

        except Exception as e:
            print(f"Error analyzing {plan_path}: {e}")


if __name__ == "__main__":
    main()

### END ###
