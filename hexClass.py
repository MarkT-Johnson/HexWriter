import math
import tkinter as tk
from math import cos, sin, pi, sqrt, ceil


class Hexagram:
    Point = list[float]  # A two element list of floats representing a coordinate

    canvas_size = None
    canvas = None

    # Modifiers needed to draw the starters and secondary origin. All Hexes should share the same mods
    primary_starter_mod = [0.0, 0.0]
    secondary_origin_mod = [0.0, 0.0]
    secondary_starter_mod = [0.0, 0.0]

    origin = None

    point_mod_rots = [0,  # Tri 1
                      60,  # Tri 2
                      120,  # Tri 3
                      180,  # Tri 4
                      240,  # Tri 5
                      300]  # Tri 6

    hexagram_count = 0

    def __init__(self, lines: list[str], hex_number: int, canvas_sz: int = None, canvas: tk.Canvas = None):
        """
        Initializes a new hexagram around the origin point with several lines
        :param canvas_sz: The dimension of the canvas (first hex only)
        :param canvas: The canvas the hexagrams are being drawn on (first hex only)
        :param lines: List of which lines should be drawn per triangle [[1, 2, 3, 4], [1, 2, 3, 4], ...]
        """
        Hexagram.canvas_size = Hexagram.canvas_size if canvas_sz is None else canvas_sz  # If we already have a canvas_size, we dont need to instantiate a new one.
        Hexagram.canvas = Hexagram.canvas if canvas is None else canvas  # If we already have a canvas, we dont need to instantiate a new one.
        self.lines = lines
        self.hex_number = hex_number   # Track which Hex this object is starting at one
        Hexagram._update_mods(self)
        self.draw_hex()

    def _update_mods(self):
        """
        Updates the common modifiers used by all hexagrams when drawn (class origin, primary_starter_mod,
        secondary_origin_mod, secondary_starter_mod), as well as updating the instance specific origin based
        on which number of hex this instance of a hexagram is
        :return: None
        """
        # l = Length of primary sides
        l = Hexagram.canvas_size / 10
        # h = height of a triangle
        h = (sqrt(3)*l)/2

        # Determine the class origin, from which the individual hexagrams will base their own origins around
        Hexagram.origin = [Hexagram.canvas_size / 2, Hexagram.canvas_size / 2]

        # Distance that each origin is offset from the other
        origin_offset = (l * 2) - (l / 9)

        # self.origin_mod = [0.0, 0.0]

        # TODO: Figure out how to determine the correct angle for the bearing
        # Calculate the instance version of the origin based on hex_number
        new_origin = [0.0, 0.0]

        # This mechanism should work for hexes 1-7 but after that it falls apart
        if self.hex_number > 1:
            heading = 30
            heading += (self.hex_number - 2) * 60
            new_origin = self._rotate_point([0.0, -origin_offset], [0.0, 0.0], heading)

        self.origin_mod = new_origin

        # Modifiers needed to draw the starters and secondary origin. All Hexes should share the same mods
        Hexagram.primary_starter_mod = [0, -l]
        Hexagram.secondary_origin_mod = [l / 9, -l / 6]
        Hexagram.secondary_starter_mod = [l / 9, -5 * l / 6]

    def _bearing(self, start: Point, degrees: float, dist: float) -> Point:
        """
        Calculates a new point based off a intitial point given a bearing and distance.
        x` = [ Sin(rad) * dist ] + x
        y` = [ Cos(rad) * dist ] + y
        :param start_p: Intitial point being measured from
        :param degrees: The bearing we are going (in degrees)
        :param dist: The distance we are going
        :return: The coordinates of the new point
        """
        # Convert degrees to radians
        radians = degrees * pi / 180

        # Get new x` and y`
        x_p = (sin(radians) * dist) + start[0]
        y_p = (cos(radians) * dist) + start[1]

        return [x_p, y_p]

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
        return Hexagram.canvas.create_oval(x1, y1, x2, y2, fill=color, outline=color)

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
        # Translate point, so we can rotate about [0, 0]
        trans_point = self._sub_points(point, origin)

        # Convert degrees to radians
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
        primary_origin = self._add_points(Hexagram.origin, self.origin_mod)
        primary_starter = self._add_points(primary_origin, Hexagram.primary_starter_mod)
        secondary_origin = self._add_points(primary_origin, Hexagram.secondary_origin_mod)
        secondary_starter = self._add_points(primary_origin, Hexagram.secondary_starter_mod)

        for tri in range(0, 6):
            rot = Hexagram.point_mod_rots[tri]

            # Create primary points
            curr_primary = self._rotate_point(primary_starter, primary_origin, rot)
            next_primary = self._rotate_point(curr_primary, primary_origin, 60)

            # Create secondary points
            curr_sec_origin = self._rotate_point(secondary_origin, primary_origin, rot)
            curr_sec_outer1 = self._rotate_point(secondary_starter, primary_origin, rot)
            curr_sec_outer2 = self._rotate_point(curr_sec_outer1, curr_sec_origin, 60)  # We rotate around curr_sec_origin since the
                                                                                        # 60 degrees here refers to angle
                                                                                        # (curr_sec_outer1, curr_sec_origin, curr_sec_outer2)
            width = 3
            # For each line in the current triangle, determine if it should be drawn
            if self.lines[tri][0] == "1":   # Draw line 1
                Hexagram.canvas.create_line(primary_origin + curr_primary, fill="orange", width=width)
            if self.lines[tri][1] == "1":   # Draw line 2
                Hexagram.canvas.create_line(curr_sec_origin + curr_sec_outer1, fill="orange", width=width)
            if self.lines[tri][2] == "1":   # Draw line 3
                Hexagram.canvas.create_line(curr_primary + next_primary, fill="green", width=width)
            if self.lines[tri][3] == "1":   # Draw line 4
                Hexagram.canvas.create_line(curr_sec_outer1 + curr_sec_outer2, fill="green", width=width)
