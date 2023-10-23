#!/usr/bin/env python3

"""

TOPOLOGY DEBUGGING

To run:

$ ./topodebug.py

https://pypi.org/project/javascript/

Prerequisites:

npm install -g topojson-client
pip install javascript

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

from typing import Any

from rdafn import *


topojson = require("topojson-client")

# Read the state topology & index the features by GEOID

# topo_path: str = "temp/NC_vtd_topo.json"
topo_path: str = "temp/NC_vtd_simple_topo.json"
# topo_path: str = "temp/NC_vtd_quantized_topo.json"

state_topo: dict[str, Any] = read_json(topo_path)
fc = state_topo["objects"]["collection"]["geometries"]

feature_index: dict[str, int] = dict()
for i, vtd in enumerate(fc):
    geoid: str = vtd["properties"]["GEOID20"]
    feature_index[geoid] = i

# Read a plan & invert it by district #

plan_path: str = "data/NC/NC20C_baseline_100.csv"
plan: list[dict[str, Any]] = load_plan(plan_path).assignments

precincts_by_district: dict[int, set[str]] = defaultdict(set)
for row in plan:
    precincts_by_district[row["DISTRICT"]].add(row["GEOID"])

"""
### TEST ###

merged_geojson: dict[str, Any] | None = topojson.merge(state_topo, fc).valueOf()

shp: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | LinearRing | GeometryCollection = shape(
    merged_geojson
)

compactness_metrics: dict = rda.calc_compactness([shp])
print(compactness_metrics)

pass
"""

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
    if i != 6:  # TODO
        continue

    district_features: list = [fc[i] for i in map(feature_index.get, precincts)]
    merged_geojson: dict[str, Any] | None = topojson.merge(
        state_topo, district_features
    ).valueOf()
    shp: Point | MultiPoint | LineString | MultiLineString | Polygon | MultiPolygon | LinearRing | GeometryCollection = shape(
        merged_geojson
    )
    district_shapes.append(shp)

    try:
        rda.calc_compactness([shp])
        print(f"Calculated compactness on district {i}")
    except:
        print(f"Exception calculating compactness on district {i}")

# compactness_metrics: dict = rda.calc_compactness(district_shapes)
# print(compactness_metrics)

pass

### END ###
