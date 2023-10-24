#!/usr/bin/env python3

"""
MAKE DISTRICT SHAPEFILES

https://pypi.org/project/geojson/
"""

from javascript import require
from shapely.geometry import (
    shape,
    Polygon,
    MultiPolygon,
    # Point,
    # MultiPoint,
    # LineString,
    # MultiLineString,
    # LinearRing,
    # GeometryCollection,
)
from collections import defaultdict
from typing import Any

topojson = require("topojson-client")


def make_district_shapes(
    topo: dict[str, Any], plan: list[dict[str, str | int]]
) -> list[
    Polygon
    | MultiPolygon
    # | Point
    # | MultiPoint
    # | LineString
    # | MultiLineString
    # | LinearRing
    # | GeometryCollection
]:
    """Make district shapes from a topology and a plan."""

    fc = topo["objects"]["collection"]["geometries"]

    feature_index: dict[str, int] = dict()
    for i, vtd in enumerate(fc):
        geoid: str = vtd["properties"]["GEOID20"]
        feature_index[geoid] = i

    precincts_by_district: dict[int, set[str]] = defaultdict(set)
    for row in plan:
        geoid: str = str(row["GEOID"])
        district: int = int(row["DISTRICT"])
        precincts_by_district[district].add(geoid)

    district_shapes: list[
        Polygon
        | MultiPolygon
        # | Point
        # | MultiPoint
        # | LineString
        # | MultiLineString
        # | LinearRing
        # | GeometryCollection
    ] = list()

    for i, precincts in precincts_by_district.items():
        if i == 6:  # TODO - Fix this!
            continue

        district_features: list = [fc[i] for i in map(feature_index.get, precincts)]

        merged_geojson: dict[str, Any] = merge_topology(topo, district_features)

        # TODO - Clean up the shapes, if necessary.
        # - Terry's correctGeometry
        # - in district-analytics/src/_api.ts -- getGoodShapes()

        shp: Polygon | MultiPolygon = shape(merged_geojson)

        district_shapes.append(shp)

    return district_shapes


def merge_topology(topo: dict[str, Any], features: list) -> dict[str, Any]:
    """Merge features into a topology."""

    merged_geojson: dict[str, Any] = topojson.merge(topo, features).valueOf()

    return merged_geojson


### END ###
