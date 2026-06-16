import pygame as pg
import const as CN
from draw import draw_line_dda

class Panel:
    def __init__(self,screen, width, height, bg_color=(255,255,255)):
        self.surface = pg.Surface((width, height))
        self.width = width
        self.height = height
        self.screen = screen
        self.pixels = []
        self.bg_color = bg_color
        for r in range(self.height):
            row = []
            for c in range(self.width):
                row.append(self.bg_color)
            self.pixels.append(row)

    def get_coords(self):
        pass

    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None
    def set_pixel(self, x, y, color=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.pixels[y][x] = color if color else self.bg_color

    def draw(self):
      pass



class Canvas(Panel):
    def __init__(self, screen, width, height, bg_color=(255,255,255)):
        super().__init__(screen, width, height, bg_color)

    def get_coords(self):
        x, y = pg.mouse.get_pos()
        canvas_x = x // CN.CELL_SIZE
        canvas_y = (y - 80)  // CN.CELL_SIZE
        return Point2D(canvas_x, canvas_y)

    def draw(self):
        for x in range(self.height):
            for y in range (self.width):
                # color = self.get_pixel(x, y)
                color = self.pixels[y][x]
                rect = pg.Rect(x * CN.CELL_SIZE, y * CN.CELL_SIZE + 80, CN.CELL_SIZE, CN.CELL_SIZE)

                pg.draw.rect(self.screen, color, rect)
                if CN.CELL_SIZE >= 3:
                    pg.draw.rect(self.screen, (200, 200, 200), rect, 1)

    def draw_line(self, p1, p2, color, thickness=1, antialiasing=True):
        draw_line_dda(p1, p2, p2, color, thickness, antialiasing)




class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coords(self):
        pass



class Point2D(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def conv(self):
        return self.x, self.y



class Shape:
    def __init__(self, color):
        self.color = color

    def draw(self, surface):
        pass



class Shape2D(Shape):
    def __init__(self, color, points):
        super().__init__(color)
        self.points = points



class Polygon2D(Shape2D):
    def __init__(self, color, points):
        super().__init__(color, points)

    def draw(self, surface):
        if len(self.points) < 2:
            return
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            draw_line_dda(surface, p1, p2, self.color)



class Parallelogram(Polygon2D):
    def __init__(self, p1, p2, p3, p4, color):
        points = [p1, p2, p3, p4]
        super().__init__(color, points)




class Rectangle(Parallelogram):
    def __init__(self,x1, y1, x2, y2, color):
        p1 = Point2D(x1, y1)
        p2 = Point2D(x2, y1)
        p3 = Point2D(x2, y2)
        p4 = Point2D(x1, y2)
        super().__init__(p1, p2, p3, p4, color)



class Rhombus(Parallelogram):
    def __init__(self, center, width, height, color):
        cx, cy = center.get_coords()
        p1 = Point2D(cx, cy - height // 2)
        p2 = Point2D(cx + width // 2, cy)
        p3 = Point2D(cx, cy + height // 2)
        p4 = Point2D(cx - width // 2, cy)
        super().__init__(p1, p2, p3, p4, color)



class Square(Rhombus):
    def __init__(self, center, size,  color):
        super().__init__(center, size, size, color)