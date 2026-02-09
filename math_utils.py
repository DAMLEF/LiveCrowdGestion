from typing import Tuple, List, Any, Union

import math


# Functions
def ramp(x: float) -> float:
    return max(0., x)

# Vector treatment
def norm(vector: List[Any]) -> float:
    return math.sqrt(vector[0] ** 2 + vector[1] ** 2)

def normalize(vector: List[Any]) -> List[Union[float, Any]]:
    n = norm(vector)
    return [vector[0] / n, vector[1] / n ]

def dot(vector: List[Any], other: List[Any]) -> Any:
    return vector[0] * other[0] + vector[1] * other[1]

# ------------------------------------------------

# Polygon treatment
def distance_point_to_segment(point: tuple, A: tuple, B: tuple) -> Tuple[float, tuple]:
    """
    Returns the minimum distance between point P and the segment AB,
    as well as the closest point on the segment to P.
    """

    # Vectors
    APx, APy = point[0] - A[0], point[1] - A[1]
    ABx, ABy = B[0] - A[0], B[1] - A[1]

    AB_len2 = ABx ** 2 + ABy ** 2

    if AB_len2 == 0:
        # Case A == B
        closest_point = A
        dist = math.hypot(APx, APy)
        return dist, closest_point

    # Parameter t of the projection of P onto AB
    t = (APx * ABx + APy * ABy) / AB_len2
    t = max(0.0, min(1.0, t))  # clamp t between 0 and 1

    # Point projected onto the segment
    closest_x = A[0] + t * ABx
    closest_y = A[1] + t * ABy
    closest_point = (closest_x, closest_y)

    # Euclidean distance
    dist = math.hypot(point[0] - closest_x, point[1] - closest_y)
    return dist, closest_point


def nearest_impact_point_polygon(point: tuple, polygon: List[tuple]):
        """
        Returns the minimum distance between point P and the polygon poly,
        as well as the closest point on the polygon to P.
        """
        min_dist = float("inf")
        closest_point = None
        n = len(polygon)

        for i in range(n):
            A = polygon[i]
            B = polygon[(i + 1) % n]

            dist, pt = distance_point_to_segment(point, A, B)

            if dist < min_dist:
                min_dist = dist
                closest_point = pt

        return min_dist, closest_point
