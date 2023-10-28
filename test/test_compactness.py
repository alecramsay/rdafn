#!/usr/bin/env python3

"""
TEST COMPACTNESS
"""

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

import rdapy as rda

from rdafn.readwrite import read_json
from rdafn.districtshapes import geojson_to_shape
from testutils import *


class TestCompactness:
    def test_NC_116th(self) -> None:
        shapes_path = "testdata/compactness/NC-116th-Congressional.geojson"
        geojson = read_json(shapes_path)

        expected_path = "testdata/compactness/NC-116th-Congressional.json"
        expected = read_json(expected_path)

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

        for f in geojson["features"]:
            shp: Polygon | MultiPolygon = geojson_to_shape(f["geometry"])

            district_shapes.append(shp)

        actual: dict[str, Any] = rda.calc_compactness(district_shapes)

        assert approx_equal(actual["avgReock"], expected["avgReock"], places=2)
        assert approx_equal(actual["avgPolsby"], expected["avgPolsby"], places=2)
        assert approx_equal(actual["avgKIWYSI"], expected["avgKIWYSI"], places=2)

        for i in range(len(actual["byDistrict"])):
            assert approx_equal(
                actual["byDistrict"][i]["reock"],
                expected["byDistrict"][i]["reock"],
                places=2,
            )
            assert approx_equal(
                actual["byDistrict"][i]["polsby"],
                expected["byDistrict"][i]["polsby"],
                places=2,
            )
            assert approx_equal(
                round(actual["byDistrict"][i]["kiwysiRank"]),
                round(expected["byDistrict"][i]["kiwysiRank"]),
                places=2,
            )


### END ###
