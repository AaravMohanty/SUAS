import math
from typing import List, Tuple


def squared_polar(
    point: Tuple[float, float], centre: Tuple[float, float]
) -> Tuple[float, float]:
    return [
        math.atan2(point[1] - centre[1], point[0] - centre[0]),
        (point[0] - centre[0]) ** 2 + (point[1] - centre[1]) ** 2,  # Square of distance
    ]


# f([(lat,long,alt)]) -> [(lat,long,alt)] # ordered list in path order
def poly_sort(
    points: List[Tuple[float, float, float]]
) -> List[Tuple[float, float, float]]:
    # Get "centre of mass"
    centre = [
        sum(p[0] for p in points) / len(points),
        sum(p[1] for p in points) / len(points),
    ]
    new_points: List[tuple, tuple, tuple, tuple] = []  # (x,y,theta,r)

    # Sort by polar angle and distance, centered at this centre of mass.
    for point in points:
        (theta, r) = squared_polar(point, centre)
        new_points.append((point[0], point[1], point[2], theta, r))
    new_points.sort(key=lambda p: (p[3], p[4]))

    return [(point[0], point[1], point[2]) for point in new_points]


# rotate the path's ordered list so that the starting point is first
def rotate_to_starting_point(
    points: List[Tuple[float, float, float]], starting_point: Tuple[float, float, float]
):
    i = 0
    while not (
        math.isclose(points[0][0], starting_point[0])
        and math.isclose(points[0][1], starting_point[1])
        and math.isclose(points[0][2], starting_point[2])
    ):
        points = points[1:] + [points[0]]
        if i > len(points):
            print("Starting point is not in the list of points.")
            return ValueError()
        i += 1
    return points


# put in coords of targets, get path with starting point as its beginning as an ordered list of coords
def get_path(
    targets: List[Tuple[float, float, float]],
    starting_point: Tuple[float, float, float],
) -> List[Tuple[float, float, float]]:
    points = poly_sort(targets + [starting_point])
    return rotate_to_starting_point(points, starting_point)


# lat, long, altitude(feet)
coordsLatLong = [
    [38.31594832826572, -76.55657341657302, 80],
    [38.31546739500083, -76.55376201277696, 80],
    [38.31470980862425, -76.54936361414539, 80],
    [38.31424154692598, -76.54662761646904, 80],
    [38.31369801280048, -76.54342380058223, 80],
    [38.3131079191371, -76.54109648475954, 80],
    [38.31529941346197, -76.54052104837133, 80],
    [38.31587643291039, -76.54361305817427, 80],
    [38.31861642463319, -76.54538594175376, 80],
    [38.31862683616554, -76.55206138505936, 80],
    [38.31703471119464, -76.55244787859773, 80],
    [38.31674255749409, -76.55294546866578, 80],
]
startingPoint = [38.31729702009844, -76.55617670782419, 0]

import random


def generate_coordinates(n=20):
    coordinates = []
    for _ in range(n):
        lat = random.uniform(38.31, 38.32)
        lon = random.uniform(-76.55, -76.54)
        alt = random.uniform(80, 120)
        coordinates.append((lat, lon, alt))
    return coordinates


random_coords = generate_coordinates(100)

# rotate the path until the starting point is first.

import matplotlib.pyplot as plt


def display_polygon(points):
    # Assuming points are in the order of the polygon vertices
    points.append(points[0])  # repeat the first point to create a 'closed loop'

    xs, ys = zip(
        *[(point[0], point[1]) for point in points]
    )  # create lists of x and y values

    plt.figure()
    plt.plot(xs, ys)
    plt.show()  # display


from mpl_toolkits.mplot3d import Axes3D


def display_polygon_3d(points):
    fig = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection="3d")

    xs, ys, zs = zip(*(points + [points[0]]))  # create lists of x, y and z values

    ax.plot(xs, ys, zs)
    ax.set_zlim(0, 200)
    plt.show()  # display


# Example usage:
# path = poly_sort(coordsLatLong + [startingPoint])
path = get_path(random_coords, startingPoint)
print(path[0])

# display_polygon(path)
display_polygon_3d(path)
