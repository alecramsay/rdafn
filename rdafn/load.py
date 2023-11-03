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


def load_shapes(xx: str) -> dict[str, dict[str, Any]]:
    """Load preprocessed shape data."""

    pickle_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "shapes"], "_", "pickle"
    )

    shapes: dict[str, dict[str, Any]] = read_pickle(pickle_path)

    return shapes


def load_graph(xx: str) -> dict[str, list[str]]:
    """Load the graph for a state."""

    graph_path: str = path_to_file([data_dir, xx]) + file_name(
        [xx, cycle, "graph"], "_", "json"
    )
    graph: dict[str, list[str]] = read_json(graph_path)

    return graph


def load_topology(xx: str) -> dict[str, Any]:
    """Load the topology for a state."""

    topo_file: str = f"{xx}_vtd_simple_topo.json"
    # topo_file: str = f"{xx}_vtd_topo.json"
    # topo_file: str = f"{xx}_vtd_quantized_topo.json"
    topo_path: str = path_to_file([data_dir, xx]) + topo_file

    topo: dict[str, Any] = read_json(topo_path)

    return topo


def load_plan(plan_file: str) -> list[dict[str, int]]:
    """Read a precinct-assignment file."""

    assignments: list[dict[str, int]] = read_csv(plan_file, [str, int])

    return assignments


### END ###
