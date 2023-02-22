import pandas as pd
import h3
from pathlib import Path
from typing import Dict, List, Union
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from schemas import point_schema, polygon_schema


class GeoAggr:
    def __init__(self) -> None:
        self.data: pd.DataFrame = pd.read_csv(Path.cwd().joinpath("data/apartments.csv"), delimiter=",")
        self.point_schema = point_schema
        self.polygon_schema = polygon_schema

    def aggr_hexs(self, geometry: Dict[str, Union[str, List[Union[float, int]]]], field: str,
                  aggr: str, r: int) -> Union[int, float, str]:

        errors = dict()

        try:
            validate(geometry, self.point_schema)
        except ValidationError:
            errors["Wrong_geometry_parameter"] = "must be {'type': 'Point', 'coordinates': [int or float, int or float]}"

        if r < 0:
            errors["Wrong r parameter"] = "must be positive or 0"

        if self.data.get(field) is None:
            errors["Wrong field parameter"] = f"must be {' or '.join(self.data.keys()[2:])}"

        if (aggr != "sum") and (aggr != "avg") and (aggr != "max") and (aggr != "min"):
            errors["Wrong aggr parameter"] = "must be sum or avg or max or min"

        if errors:
            raise ValueError(errors)

        hexes = h3.k_ring(h3.geo_to_h3(lat=geometry["coordinates"][1], lng=geometry["coordinates"][0],
                                       resolution=11), k=r)

        result = []

        for v in zip(self.data["geopos"], self.data[field]):
            geometry_geojson = eval(v[0])
            cur_hex = h3.geo_to_h3(lat=geometry_geojson["coordinates"][1], lng=geometry_geojson["coordinates"][0],
                                   resolution=11)
            if cur_hex in hexes:
                result.append(v[1])

        if aggr == "sum":
            if not result:
                return "there are no objects in the specified radius from this point"
            else:
                return sum(result)
        elif aggr == "avg":
            if not result:
                return "there are no objects in the specified radius from this point"
            else:
                return sum(result) / len(result)
        elif aggr == "max":
            if not result:
                return "there are no objects in the specified radius from this point"
            else:
                max(result)
        elif aggr == "min":
            if not result:
                return "there are no objects in the specified radius from this point"
            else:
                min(result)

    def aggr_polygon(self, geometry: Dict[str, Union[str, List[List[List[Union[int, float]]]]]],
                     field: str, aggr: str) -> Union[int, float, str]:
        errors = dict()

        try:
            validate(geometry, self.polygon_schema)
        except ValidationError:
            errors["Wrong geometry parameter"] = "must be {'type': 'Polygon', 'coordinates': [[[int or float, int or float], ...], ...]}"

        if self.data.get(field) is None:
            errors["Wrong field parameter"] = f"must be {' or '.join(self.data.keys()[2:])}"

        if (aggr != "sum") and (aggr != "avg") and (aggr != "max") and (aggr != "min"):
            errors["Wrong aggr parameter"] = "must be sum or avg or max or min"

        if errors:
            raise ValueError(errors)

        hexes = list(h3.polyfill(geometry, 11))

        result = []

        for v in zip(self.data["geopos"], self.data[field]):
            geometry_geojson = eval(v[0])
            cur_hex = h3.geo_to_h3(lat=geometry_geojson["coordinates"][0], lng=geometry_geojson["coordinates"][1],
                                   resolution=11)

            if cur_hex in hexes:
                result.append(v[1])

        if aggr == "sum":
            if not result:
                return "there are no objects in this polygon"
            else:
                return sum(result)
        elif aggr == "avg":
            if not result:
                return "there are no objects in this polygon"
            else:
                return sum(result) / len(result)
        elif aggr == "max":
            if not result:
                return "there are no objects in this polygon"
            else:
                max(result)
        elif aggr == "min":
            if not result:
                return "there are no objects in this polygon"
            else:
                min(result)
