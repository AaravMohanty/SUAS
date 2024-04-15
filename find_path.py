# f(GPSData) -> (x,y)
# f([(x,y)]) -> [(x,y)]

import math


def squared_polar(point, centre):
    return [
        math.atan2(point[1] - centre[1], point[0] - centre[0]),
        (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2,  # Square of distance
    ]


def poly_sort(points):
    # Get "centre of mass"
    centre = [
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
    ]

    # Sort by polar angle and distance, centered at this centre of mass.
    for point in points:
        point.extend(squared_polar(point, centre))
    points.sort(key=lambda p: (p[2], p[3]))

    # Throw away the temporary polar coordinates
    for point in points:
        point.pop()
        point.pop()
