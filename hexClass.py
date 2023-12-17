import tkinter as tk
from math import cos, sin, pi, sqrt


class Hexagram:
    Point = list[float]  # A two element list of integers representing a coordinate

    canvas_size = 0
    # Modifiers needed to draw each point around the hex. All Hexes should share the same mods
    point_mods = list[Point]

    def __init__(self, origin: Point, lines: list[int], canvas_sz: int, canvas: tk.Canvas = None):
        """
        Initializes a new hexagram around the origin point with several lines
        :param canvas: The canvas this hexagram is being drawn on
        :param origin: Point where the hexagram is drawn around
        :param lines: List of which lines should be drawn
        """
        self.origin = origin
        self.lines = lines
        Hexagram.canvas_size = canvas_sz  # When creating a new hex, we may need to update the canvas size
        Hexagram.canvas = Hexagram.canvas if canvas is None else canvas  # If we already have a canvas, we dont need to instantiate a new one.
        Hexagram._update_mods()
        self.draw_hex()

    def _update_mods(self):
        # l_p = Length of primary sides
        l_p = Hexagram.canvas_size / 10
        # h_p = height of primary triangles
        h_p = (sqrt(3) * l_p) / 2

        # Modifiers needed to draw each point around the hex. All Hexes should share the same mods
        Hexagram.point_mods = [[0, -l_p],  # Point 1.1
                               [h_p, -l_p / 2],  # Point 2.1
                               [h_p, l_p / 2],  # Point 3.1
                               [0, l_p],  # Point 4.1
                               [-h_p, l_p / 2],  # Point 5.1
                               [-h_p, -l_p / 2],    # Point 6.1
                               [l_p/9, -l_p/6],     # Point 1.2
                               ]

    def _create_dot(self, point: Point, size: int = 3, color: str = "black"):
        """
        Draws a dot around the point supplied, defaults to a black dot
        :param point: The point around which the dot should be drawn
        :param size: Size of the dot (defaults to 3)
        :param color: What color to draw the dot (defaults to black)
        :return: Canvas Object ID of the dot
        """
        x1, y1 = (point[0] - size), (point[1] - size)
        x2, y2 = (point[0] + size), (point[1] + size)
        return self.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

    def _add_points(self, point1: Point, point2: Point) -> Point:
        """
        Takes in two point arrays and returns the addition of the two together.
        Ex. [1, 1] + [2, 2] = [3, 3]
        :param point1: Point 1
        :param point2: Point 2
        :return: Sum of two points
        """
        # return [round(array1[0] + array2[0]), round(array1[1] + array2[1])]
        return [point1[0] + point2[0], point1[1] + point2[1]]

    def _sub_points(self, point1: Point, point2: Point) -> Point:
        """
        Takes in two point arrays and returns the difference of the two together.
        Ex. sub_points([1, 1], [2, 2]) -> [1, 1] - [2, 2] = [-1, -1]
        :param point1: Point 1
        :param point2: Point 2
        :return: Difference of two points
        """
        return [point1[0] - point2[0], point1[1] - point2[1]]

    def _rotate_point(self, point: Point, origin: Point = [0, 0], degrees: int = 60) -> Point:
        """
        Rotates a point around an abstract origin and returns the new Point location
        :param point: Point we are going to rotate [x, y]
        :param origin: The origin we are rotating around (defaults [0,0]
        :param degrees: How far we are rotating (default 60 degrees)
        :return: New Point coordinates [x', y']
        """
        # Translate point so we can rotate about [0, 0]
        trans_point = self._sub_points(point, origin)

        radians = degrees * pi / 180

        # Calculate rotated point about the origin
        rot_point = [trans_point[0] * cos(radians) - trans_point[1] * sin(radians),
                     trans_point[1] * cos(radians) + trans_point[0] * sin(radians)]

        # Undo the initial translation after rotation
        return self._add_points(rot_point, origin)

    def draw_hex(self):
        """
        Draws the hexagram using the unique origin and lines as well as the shared canvas and point modifiers
        :return: None
        """

