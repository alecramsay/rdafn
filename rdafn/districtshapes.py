#!/usr/bin/env python3

"""
MAKE DISTRICT SHAPEFILES

Potential resources:
- https://pypi.org/project/geojson/

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
) -> list[Polygon | MultiPolygon]:
    """Make district shapes from a topology and a plan."""

    geojson: list[dict[str, Any]] = merge_features(topo, plan)
    geojson = [correct_geometry(x) for x in geojson]
    district_shapes: list[Polygon | MultiPolygon] = [
        geojson_to_shape(x) for x in geojson
    ]

    return district_shapes


def merge_features(
    topo: dict[str, Any], plan: list[dict[str, str | int]]
) -> list[dict[str, Any]]:
    """Merge precinct features into a district feature"""

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

    district_features: list[dict[str, Any]] = list()

    for i, precincts in precincts_by_district.items():
        features: list = [fc[i] for i in map(feature_index.get, precincts)]

        merged_geojson: dict[str, Any] = merge_topology(topo, features)
        district_features.append(merged_geojson)

    return district_features


def merge_topology(topo: dict[str, Any], features: list) -> dict[str, Any]:
    """Merge features into a topology."""

    merged_geojson: dict[str, Any] = topojson.merge(topo, features).valueOf()

    return merged_geojson


def correct_geometry(poly: dict[str, Any]) -> dict[str, Any]:
    """Correct the geometry of a polygon."""

    # TODO - Terry's correctGeometry
    # TODO - Also, in district-analytics/src/_api.ts -- getGoodShapes()

    return poly


def geojson_to_shape(geojson: dict[str, Any]) -> Polygon | MultiPolygon:
    """Create a Shapely shape from GeoJSON."""

    shp: Polygon | MultiPolygon = shape(geojson)

    return shp


### END ###
