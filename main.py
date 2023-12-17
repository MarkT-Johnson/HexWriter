from tkinter import *
from math import sqrt, cos, sin, pi

# How big the canvas should be
canvas_size = 1000
# l = Length of sides (10% of canvas size
l = canvas_size / 10
# h = height (simplified Herons formula and height formula)
h = (sqrt(3) * l) / 2
origin = [canvas_size / 2, canvas_size / 2]

Point = list[float]

sec_origin_mod = [l / 9, -l / 6]

# Modifiers needed to draw each point around the hex
point_mods = [[0, -l],  # Point 1
              [h, -l / 2],  # Point 2
              [h, l / 2],  # Point 3
              [0, l],  # Point 4
              [-h, l / 2],  # Point 5
              [-h, -l / 2]]  # Point 6

point_mod_rots = [0,  # Tri 1
                  60,  # Tri 2
                  120,  # Tri 3
                  180,  # Tri 4
                  240,  # Tri 5
                  300]  # Tri 6


def add_points(point1: Point, point2: Point) -> Point:
    """
    Takes in two point arrays and returns the addition of the two together.
    Ex. add_points([1, 1], [2, 2]) -> [1, 1] + [2, 2] = [3, 3]
    :param point1: Point 1
    :param point2: Point 2
    :return: Sum of two points
    """
    # return [round(array1[0] + array2[0]), round(array1[1] + array2[1])]
    return [point1[0] + point2[0], point1[1] + point2[1]]


def sub_points(point1: Point, point2: Point) -> Point:
    """
    Takes in two point arrays and returns the difference of the two together.
    Ex. sub_points([1, 1], [2, 2]) -> [1, 1] - [2, 2] = [-1, -1]
    :param point1: Point 1
    :param point2: Point 2
    :return: Difference of two points
    """
    return [point1[0] - point2[0], point1[1] - point2[1]]


def create_dot(canvas: Canvas, point: Point, size: int = 3, color: str = "black"):
    """
    Draws a dot around the point supplied, defaults to a black dot
    :param canvas: Canvas on which the dot should be drawn
    :param point: The point around which the dot should be drawn
    :param size: Size of the dot (defaults to 3)
    :param color: What color to draw the dot (defaults to black)
    :return: Canvas Object ID of the dot
    """
    x1, y1 = (point[0] - size), (point[1] - size)
    x2, y2 = (point[0] + size), (point[1] + size)
    return canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)


def rotate_point(point: Point, origin: Point, degrees: int) -> Point:
    """
    Rotates a point around an abstract origin and returns the new Point location.
    "Rotate POINT about ORIGIN by DEGREES"
    :param point: Point we are going to rotate [x, y]
    :param origin: The origin we are rotating around [j, k]
    :param degrees: How far we are rotating (in degrees)
    :return: New Point coordinates [x', y']
    """
    # Translate point so we can rotate about [0, 0]
    trans_point = sub_points(point, origin)

    radians = degrees * pi / 180

    # Calculate rotated point about the origin
    rot_point = [trans_point[0] * cos(radians) - trans_point[1] * sin(radians),
                 trans_point[1] * cos(radians) + trans_point[0] * sin(radians)]

    # Undo the initial translation after rotation
    return add_points(rot_point, origin)


window = Tk()

window.title("HexWriter")
window.geometry("1000x1000")

canvas = Canvas(window, width=canvas_size, height=canvas_size, bg="white")
canvas.pack()

hex_points = list()

for point in point_mods:
    modded_point = add_points(origin, point)
    hex_points = hex_points + modded_point
    # canvas.create_line(origin + modded_point, width=2, fill="orange")
    # create_dot(canvas, modded_point, color="orange")
#
# sec_origin = add_points(origin, sec_origin_mod)
# create_dot(canvas, sec_origin, color="blue")
#
# rot_origin = rotate_point(sec_origin, origin)
# create_dot(canvas,rot_origin, color="red")

primary_starter_mod = [0, -l]
secondary_origin_mod = [l / 9, -l / 6]
secondary_starter_mod = [l / 9, -5 * l / 6]

primary_starter = add_points(origin, primary_starter_mod)
secondary_origin = add_points(origin, sec_origin_mod)
secondary_starter = add_points(origin, secondary_starter_mod)

for rot in point_mod_rots:
    # Create primary points
    curr_primary = rotate_point(primary_starter, origin, rot)
    next_primary = rotate_point(curr_primary, origin, 60)

    # Create secondary points
    curr_sec_origin = rotate_point(secondary_origin, origin, rot)
    curr_sec_outer1 = rotate_point(secondary_starter, origin, rot)
    curr_sec_outer2 = rotate_point(curr_sec_outer1, curr_sec_origin, 60)    # We rotate around curr_sec_origin since the
                                                                            # 60 degrees here refers to angle
                                                                            # (curr_sec_outer1, curr_sec_origin, curr_sec_outer2)

    # TODO: Insert logic for deciding which lines to draw
    # TEMP: Draw ALL THE LINES!
    width = 3
    canvas.create_line(origin + curr_primary, fill="orange", width=width)
    canvas.create_line(curr_primary + next_primary, fill="green", width=width)
    canvas.create_line(curr_sec_origin + curr_sec_outer1, fill="orange", width=width)
    canvas.create_line(curr_sec_outer1 + curr_sec_outer2, fill="green", width=width)

    # Draw the dots
    # create_dot(canvas, curr_primary)
    # # Skip next_primary since it will be drawn in the next iteration as curr_primary
    # create_dot(canvas, curr_sec_origin)
    # create_dot(canvas, curr_sec_outer1)
    # create_dot(canvas, curr_sec_outer2)

create_dot(canvas, origin)
canvas.tag_lower(canvas.create_polygon(hex_points, outline="grey", fill="white", width=2))  # Draw outline hex

window.mainloop()
