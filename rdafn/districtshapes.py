#!/usr/bin/env python3

"""
MAKE DISTRICT SHAPEFILES
"""

from javascript import require
from shapely.geometry import (
    shape,
    Polygon,
    MultiPolygon,
    Point,
    MultiPoint,
    LineString,
    MultiLineString,
    LinearRing,
    GeometryCollection,
)
from collections import defaultdict
from typing import Any


def make_district_shapes(
    topo: dict[str, Any], plan: list[dict[str, str | int]]
) -> list[
    Point
    | MultiPoint
    | LineString
    | MultiLineString
    | Polygon
    | MultiPolygon
    | LinearRing
    | GeometryCollection
]:
    """Make district shapes from a topology and a plan."""

    topojson = require("topojson-client")
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
        Point
        | MultiPoint
        | LineString
        | MultiLineString
        | Polygon
        | MultiPolygon
        | LinearRing
        | GeometryCollection
    ] = list()

    for i, precincts in precincts_by_district.items():
        if i == 6:  # TODO - Fix this!
            continue

        district_features: list = [fc[i] for i in map(feature_index.get, precincts)]

        # TODO - Factor this!
        merged_geojson: dict[str, Any] | None = topojson.merge(
            topo, district_features
        ).valueOf()
        shp: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | LinearRing | GeometryCollection = shape(
            merged_geojson
        )
        district_shapes.append(shp)

    return district_shapes


### END ###
