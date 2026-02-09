from __future__ import annotations
from abc import ABC, abstractmethod
from math import sqrt, radians, sin, cos, asin
from typing import Tuple

Point = Tuple[float, float]

class Distance(ABC):
    @abstractmethod
    def between(self, a: Point, b: Point) -> float: ...

class Euclidean(Distance):
    # TODO
    def between(self, a: Point, b: Point) -> float:
        ax, ay = a
        bx, by = b
        return sqrt((ax - bx) ** 2 + (ay - by ) ** 2)

class Manhattan(Distance):
    # TODO
    def between(self, a: Point, b: Point) -> float:
        ax, ay = a
        bx, by = b
        return abs(ax - bx) + abs(ay - by)

class GreatCircle(Distance):
    """Treat points as (lat, lon) in degrees; return km (R=6371.0088)."""
    # TODO (haversine)
    R=6371.0088

    def between(self, a: Point, b: Point) -> float:
        lat1, lon1 = a
        lat2, lon2 = b

        lat1 = radians(lat1)
        lon1 = radians(lon1)
        lat2 = radians(lat2)
        lon2 = radians(lon2)

        dlat = lat2 = lat1
        dlon = lon2 - lon1

        h = (
            sin(dlat / 2) ** 2
            + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        )

        return 2 * self.R * asin(h ** 0.5)


def compare_profiles(metric: Distance, a: Point, b: Point) -> float:
    # TODO: delegate to metric
    return metric.between(a, b)
