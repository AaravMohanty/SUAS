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


coordsLatLong = [
[38.31594832826572, -76.55657341657302, 0],
[38.31546739500083, -76.55376201277696, 0],
[38.31470980862425, -76.54936361414539, 0],
[38.31424154692598, -76.54662761646904, 0],
[38.31369801280048, -76.54342380058223, 0],
[38.31331079191371, -76.54109648475954, 0],
[38.31529941346197, -76.54052104837133, 0],
[38.31587643291039, -76.54361305817427, 0],
[38.31861642463319, -76.54538594175376, 0],
[38.31862683616554, -76.55206138505936, 0],
[38.31703471119464, -76.55244787859773, 0],
[38.31674255749409, -76.55294546866578, 0]]
startingPoint = [38.31729702009844, -76.55617670782419, 0]