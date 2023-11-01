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

# from .utils import *

topojson = require("topojson-client")


# @time_function
def make_district_shapes(
    topo: dict[str, Any], plan: list[dict[str, str | int]]
) -> list[Polygon | MultiPolygon]:
    """Make district shapes from a topology and a plan."""

    district_geojsons: list[dict[str, Any]] = merge_features(topo, plan)
    # district_geojsons = [correct_geometry(x) for x in district_geojsons] # TODO - Not implemented yet
    # district_geojsons = [canonicalize_format(x) for x in district_geojsons] # TODO - Not implemented yet
    district_shapes: list[Polygon | MultiPolygon] = [
        geojson_to_shape(x) for x in district_geojsons
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
    """Correct the geometry of a polygon.

    # TODO - Terry's correctGeometry
    """

    return poly


def canonicalize_format(poly: dict[str, Any]) -> dict[str, Any]:
    """Canonicalize GeoJSON.

    # TODO - Also, in district-analytics/src/_api.ts -- getGoodShapes():

    getGoodShapes(): T.GeoFeatureCollection
    {
        const rawShapes = this.districts.getDistrictShapes();

        // Filter the real shapes & throw everything else away
        let goodShapes = {} as T.GeoFeatureCollection;
        goodShapes['type'] = "FeatureCollection";
        goodShapes['features'] = [] as T.GeoFeatureArray;

        for (let i = 0; i < rawShapes.features.length; i++)
        {
        const shape: any = rawShapes.features[i];

        if (isAShape(shape))
        {
            const d = Poly.polyDescribe(shape);

            let f: any = {
            type: 'Feature',
            properties: {districtID: `${i + 1}`},
            geometry: {
                type: (d.npoly > 1) ? 'MultiPolygon' : 'Polygon',
                coordinates: shape.geometry.coordinates
            }
            };
            goodShapes.features.push(f);
        }
        }

        return goodShapes;
    }

    function isAShape(poly: any): boolean
    {
        if (poly == null) return false;
        if (Poly.polyNull(poly)) return false;
        return poly.geometry && poly.geometry.coordinates && !U.isArrayEmpty(poly.geometry.coordinates);
    }
    """

    return poly


def geojson_to_shape(geojson: dict[str, Any]) -> Polygon | MultiPolygon:
    """Create a Shapely shape from GeoJSON."""

    shp: Polygon | MultiPolygon = shape(geojson)

    return shp


### END ###
