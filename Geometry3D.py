import math
from Draw import draw_line_dda
from Geometry import Point2D
import Constant as Cn
from Toolbar import Palette

CUBE_VERTICES = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1),  (1, -1, 1),  (1, 1, 1),  (-1, 1, 1)
]


CUBE_EDGES = [
    (0,1), (1,2), (2,3), (3,0),
    (4,5), (5,6), (6,7), (7,4),
    (0,4), (1,5), (2,6), (3,7)
]


PIRAMID3_EDGES = [
    (0,1), (0,2), (0,3),
    (1,2), (1,3), (2,3)
]
#
#
# def draw_cube(canvas, center_x, center_y, size, color=Cn.BLACK):
#
#     angle = math.radians(30)
#     cos_a = math.cos(angle)
#     sin_a = math.sin(angle)
#

class Cube:
    def __init__(self, surface, p, size, angle, color):
        self.cube_edges = CUBE_EDGES
        self.points = [p]
        self.angle = math.radians(angle)
        self.size = size
        self.color = color
        self.surface = surface
        self.create_points()

    def create_points(self):
        x, y = self.points[0].conv()
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)
        self.points.append(Point2D(x + self.size, y))
        self.points.append(Point2D(x + self.size, y + self.size))
        self.points.append(Point2D(x, y + self.size))
        self.points.append(Point2D(x + self.size * cos, y - self.size * sin))
        x, y = self.points[-1].conv()
        self.points.append(Point2D(x + self.size, y))
        self.points.append(Point2D(x + self.size, y + self.size))
        self.points.append(Point2D(x, y + self.size))

    def draw(self):
        for edge, end_edges in self.cube_edges:
            start_p = self.points[edge]
            end_p = self.points[end_edges]
            draw_line_dda(self.surface, start_p, end_p, self.color)



class Piramid3:
    def __init__(self, surface, p, angle, size, color):
        self.points = [p]
        self.angle = math.radians(angle)
        self.color = color
        self.p_edges = PIRAMID3_EDGES
        self.surface = surface
        self.size = size
        self.create_points()

    def create_points(self):
        x, y = self.points[0].conv()
        sin = math.sin(self.angle)
        cos = math.cos(self.angle)
        self.points.append(Point2D(x, y - self.size))
        self.points.append(Point2D(x - self.size * cos * 0.9, y + self.size * sin * 0.9))
        x, y = self.points[-1].conv()
        self.points.append(Point2D(x + self.size, y))

    def draw(self):
        for edge, end_edges in self.p_edges:
            start_p = self.points[edge]
            end_p = self.points[end_edges]
            draw_line_dda(self.surface, start_p, end_p, self.color)








