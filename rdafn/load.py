#!/usr/bin/env python3

"""
LOAD HELPERS
"""

from typing import Any
import rdadata as rdd

# TODO
# from .constants import *
# from .readwrite import *


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data."""

    pickle_path: str = rdd.path_to_file([rdd.data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "data"], "_", "pickle"
    )

    data: dict[str, dict[str, int]] = rdd.read_pickle(pickle_path)

    return data


def load_shapes(xx: str, simplified: bool = True) -> dict[str, dict[str, Any]]:
    """Load preprocessed shape data."""

    pickle_name: str = (
        f"{xx}_{rdd.cycle}_shapes_simplified.pickle"
        if simplified
        else f"{xx}_{rdd.cycle}_shapes.pickle"
    )
    pickle_path: str = rdd.path_to_file([rdd.data_dir, xx]) + pickle_name

    shapes: dict[str, dict[str, Any]] = rdd.read_pickle(pickle_path)

    return shapes


def load_graph(xx: str) -> dict[str, list[str]]:
    """Load the graph for a state."""

    graph_path: str = rdd.path_to_file([rdd.data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "graph"], "_", "json"
    )
    graph: dict[str, list[str]] = rdd.read_json(graph_path)

    return graph


def load_metadata(xx: str) -> dict[str, Any]:
    """Load metadata for a state."""

    metadata_path: str = rdd.path_to_file([rdd.data_dir, xx]) + rdd.file_name(
        [xx, rdd.cycle, "metadata"], "_", "pickle"
    )
    metadata: dict[str, Any] = rdd.read_pickle(metadata_path)

    return metadata


def load_plan(plan_file: str) -> list[dict[str, str | int]]:
    """Read a precinct-assignment file."""

    assignments: list[dict[str, str | int]] = rdd.read_csv(plan_file, [str, int])

    return assignments


# NOT USED


def load_topology(xx: str) -> dict[str, Any]:
    """Load the topology for a state."""

    topo_file: str = f"{xx}_vtd_simple_topo.json"
    # topo_file: str = f"{xx}_vtd_topo.json"
    # topo_file: str = f"{xx}_vtd_quantized_topo.json"
    topo_path: str = rdd.path_to_file([rdd.data_dir, xx]) + topo_file

    topo: dict[str, Any] = rdd.read_json(topo_path)

    return topo


### END ###
