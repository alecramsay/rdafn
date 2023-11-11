#!/usr/bin/env python3

"""
LOAD HELPERS
"""

from typing import Any
import rdadata as rdd

data_project: str = "../rdadata"
shared_data_dir: str = f"{data_project}/data/"
local_data_dir: str = "data"


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data and index it by GEOID."""

    data_path: str = rdd.path_to_file([shared_data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "data"], "_", "csv"
    )
    data: list[dict] = rdd.read_csv(data_path, [str] + [int] * 13)

    indexed: dict[str, dict[str, int]] = dict()
    for row in data:
        geoid: str = row[rdd.geoid_field]
        indexed[geoid] = row

    return indexed


def load_shapes(xx: str, simplified: bool = True) -> dict[str, dict[str, Any]]:
    """Load preprocessed shape data and index it by GEOID."""

    shapes_name: str = (
        f"{xx}_{rdd.cycle}_shapes_simplified.json"
        if simplified
        else f"{xx}_{rdd.cycle}_shapes.json"
    )
    shapes_path: str = rdd.path_to_file([shared_data_dir, xx]) + shapes_name
    shapes: dict[str, dict[str, Any]] = rdd.read_json(shapes_path)

    return shapes


def load_graph(xx: str) -> dict[str, list[str]]:
    """Load the graph for a state."""

    graph_path: str = rdd.path_to_file([shared_data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "graph"], "_", "json"
    )
    graph: dict[str, list[str]] = rdd.read_json(graph_path)

    return graph


def load_metadata(xx: str) -> dict[str, Any]:
    """Load scoring-specific metadata for a state."""

    metadata_path: str = rdd.path_to_file([local_data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "metadata"], "_", "pickle"
    )
    metadata: dict[str, Any] = rdd.read_pickle(metadata_path)

    return metadata


def load_plan(plan_file: str) -> list[dict[str, str | int]]:
    """Read a precinct-assignment file."""

    assignments: list[dict[str, str | int]] = rdd.read_csv(plan_file, [str, int])

    return assignments


### END ###
