import tkinter as tk
from math import cos, sin, pi


class Hexagram:
    Point = list[float]  # A two element list of integers representing a coordinate

    canvas_size = None
    canvas = None

    # Modifiers needed to draw the starters and secondary origin. All Hexes should share the same mods
    primary_starter_mod = [0.0, 0.0]
    secondary_origin_mod = [0.0, 0.0]
    secondary_starter_mod = [0.0, 0.0]

    point_mod_rots = [0,  # Tri 1
                      60,  # Tri 2
                      120,  # Tri 3
                      180,  # Tri 4
                      240,  # Tri 5
                      300]  # Tri 6

    hexagram_count = 0

    def __init__(self, origin: Point, lines: list[list[int]], canvas_sz: int, canvas: tk.Canvas = None):
        """
        Initializes a new hexagram around the origin point with several lines
        :param canvas: The canvas this hexagram is being drawn on
        :param origin: Point where the hexagram is drawn around
        :param lines: List of which lines should be drawn per triangle [[1, 2, 3, 4], [1, 2, 3, 4]]
        """
        self.origin = origin
        self.lines = lines
        Hexagram.canvas_size = canvas_sz  # When creating a new hex, we may need to update the canvas size
        Hexagram.canvas = Hexagram.canvas if canvas is None else canvas  # If we already have a canvas, we dont need to instantiate a new one.
        Hexagram._update_mods(self)
        Hexagram.hexagram_count += 1    # Track total number of shorts
        self.hex_number = Hexagram.hexagram_count   # Track which Hex this object is
        self.draw_hex()

    def _update_mods(self):
        # l = Length of primary sides
        l = Hexagram.canvas_size / 10

        # Modifiers needed to draw the starters and secondary origin. All Hexes should share the same mods
        Hexagram.primary_starter_mod = [0, -l]
        Hexagram.secondary_origin_mod = [l / 9, -l / 6]
        Hexagram.secondary_starter_mod = [l / 9, -5 * l / 6]

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
        primary_starter = self._add_points(self.origin, Hexagram.primary_starter_mod)
        secondary_origin = self._add_points(self.origin, Hexagram.secondary_origin_mod)
        secondary_starter = self._add_points(self.origin, Hexagram.secondary_starter_mod)

        for rot in Hexagram.point_mod_rots:
            # Create primary points
            curr_primary = self._rotate_point(primary_starter, self.origin, rot)
            next_primary = self._rotate_point(curr_primary, self.origin, 60)

            # Create secondary points
            curr_sec_origin = self._rotate_point(secondary_origin, self.origin, rot)
            curr_sec_outer1 = self._rotate_point(secondary_starter, self.origin, rot)
            curr_sec_outer2 = self._rotate_point(curr_sec_outer1, curr_sec_origin, 60)  # We rotate around curr_sec_origin since the
                                                                                        # 60 degrees here refers to angle
                                                                                        # (curr_sec_outer1, curr_sec_origin, curr_sec_outer2)

            # TODO: Insert logic for deciding which lines to draw
            # TEMP: Draw ALL THE LINES!
            width = 3
            Hexagram.canvas.create_line(self.origin + curr_primary, fill="orange", width=width)
            Hexagram.canvas.create_line(curr_primary + next_primary, fill="green", width=width)
            Hexagram.canvas.create_line(curr_sec_origin + curr_sec_outer1, fill="orange", width=width)
            Hexagram.canvas.create_line(curr_sec_outer1 + curr_sec_outer2, fill="green", width=width)
