from tkinter import *
from math import sqrt, cos, sin, pi

# How big the canvas should be
canvas_size = 1000
# l = Length of sides
l = canvas_size / 10
# h = height
h = (sqrt(3) * l) / 2
origin = [canvas_size / 2, canvas_size / 2]

Point = list[float]

sec_origin_mod = [l/9, -l/6]

# Modifiers needed to draw each point around the hex
point_mods = [[0, -l],  # Point 1
              [h, -l / 2],  # Point 2
              [h, l / 2],  # Point 3
              [0, l],  # Point 4
              [-h, l / 2],  # Point 5
              [-h, -l / 2]]  # Point 6


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


def rotate_point(point: Point, origin: Point = [0, 0], degrees: int = 60) -> Point:
    """
    Rotates a point around an abstract origin and returns the new Point location
    :param point: Point we are going to rotate [x, y]
    :param origin: The origin we are rotating around (defaults [0,0]
    :param degrees: How far we are rotating (default 60 degrees)
    :return: New Point coordinates [x', y']
    """
    # Translate point so we can rotate about [0, 0]
    trans_point = sub_points(point, origin)

    radians = degrees * pi / 180

    # Calculate rotated point about the origin
    rot_point = [trans_point[0]*cos(radians) - trans_point[1]*sin(radians), trans_point[1]*cos(radians) + trans_point[0]*sin(radians)]

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
    canvas.create_line(origin + modded_point, width=2, fill="orange")
    create_dot(canvas, modded_point, color="orange")

sec_origin = add_points(origin, sec_origin_mod)
create_dot(canvas, sec_origin, color="blue")

rot_origin = rotate_point(sec_origin, origin)
create_dot(canvas,rot_origin, color="red")

create_dot(canvas, origin)
canvas.tag_lower(canvas.create_polygon(hex_points, outline="lime", fill="white", width=2))

window.mainloop()
