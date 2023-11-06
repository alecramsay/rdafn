#!/usr/bin/env python3

"""
LOAD HELPERS
"""

from .constants import *
from .readwrite import *


def load_data(xx: str) -> dict[str, dict[str, int]]:
    """Load preprocessed census & election data."""

    pickle_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "data"], "_", "pickle"
    )

    data: dict[str, dict[str, int]] = read_pickle(pickle_path)

    return data


def load_shapes(xx: str, simplified: bool = True) -> dict[str, dict[str, Any]]:
    """Load preprocessed shape data."""

    pickle_name: str = (
        f"{xx}_{cycle}_shapes_simplified.pickle"
        if simplified
        else f"{xx}_{cycle}_shapes.pickle"
    )
    pickle_path: str = path_to_file([data_dir, xx]) + pickle_name

    shapes: dict[str, dict[str, Any]] = read_pickle(pickle_path)

    return shapes


def load_graph(xx: str) -> dict[str, list[str]]:
    """Load the graph for a state."""

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "graph"], "_", "json"
    )
    graph: dict[str, list[str]] = read_json(graph_path)

    return graph


def load_metadata(xx: str) -> dict[str, Any]:
    """Load metadata for a state."""

    metadata_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "metadata"], "_", "json"
    )
    metadata: dict[str, Any] = read_json(metadata_path)

    return metadata


def load_plan(plan_file: str) -> list[dict[str, str | int]]:
    """Read a precinct-assignment file."""

    assignments: list[dict[str, str | int]] = read_csv(plan_file, [str, int])

    return assignments


# NOT USED


def load_topology(xx: str) -> dict[str, Any]:
    """Load the topology for a state."""

    topo_file: str = f"{xx}_vtd_simple_topo.json"
    # topo_file: str = f"{xx}_vtd_topo.json"
    # topo_file: str = f"{xx}_vtd_quantized_topo.json"
    topo_path: str = path_to_file([data_dir, xx]) + topo_file

    topo: dict[str, Any] = read_json(topo_path)

    return topo


### END ###
