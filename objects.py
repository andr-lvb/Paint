import pygame as pg
import const as cn
from draw import draw_line_dda
import math




class Panel:
    def __init__(self, screen, width, height, bg_color=cn.WHITE):
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

    def fill_rect(self, rect, color):
        for r in range(rect.height):
            for c in range(rect.width):
                self.set_pixel(rect.x + c, rect.y + r, color)




class Canvas(Panel):
    def __init__(self, screen, width, height, bg_color=cn.WHITE):
        super().__init__(screen, width, height, bg_color)

    def get_coords(self):
        x, y = pg.mouse.get_pos()
        canvas_x = x // cn.CELL_SIZE
        canvas_y = (y - 80) // cn.CELL_SIZE
        return Point2D(canvas_x, canvas_y)

    def draw(self):
        for x in range(self.height):
            for y in range(self.width):
                color = self.pixels[y][x]
                rect = pg.Rect(x * cn.CELL_SIZE, y * cn.CELL_SIZE + 80, cn.CELL_SIZE, cn.CELL_SIZE)

                pg.draw.rect(self.screen, color, rect)
                if cn.CELL_SIZE >= 3:
                    pg.draw.rect(self.screen, cn.COLOR_LINE_BETWEEN_CELLS, rect, 1)




class Info_Panel(Panel):
    def __init__(self, screen, width, height, bg_color=cn.BLACK):
        super().__init__(screen, width, height, bg_color)

    def draw(self):
        for x in range(self.width):
            for y in range(self.height):
                color = self.pixels[y][x]
                rect = pg.Rect(x, y, 1, 1)
                pg.draw.rect(self.screen, color, rect)

    def get_coords(self):
        x, y = pg.mouse.get_pos()
        return Point2D(x, y)




class Palette:
    def __init__(self, info_panel, colors, width, height, cell_size=30, margin=5):
        self.info_panel = info_panel
        self.colors = colors
        self.width = width
        self.height = height
        self.cell_size = cell_size
        self.margin = margin
        self.rects = []
        self.current_color = colors[2]

    def draw(self):
        cols = 4
        rows = 2
        start_x = self.margin
        start_y = self.margin
        i = 0
        for r in range(rows):
            for c in range(cols):
                x = start_x + c * (self.cell_size + self.margin)
                y = start_y + r * (self.cell_size + self.margin)
                rect = Rectangle(x, y, self.cell_size, self.cell_size, self.colors[i])
                rect.draw(self.info_panel)
                self.info_panel.fill_rect(rect, self.colors[i])
                i += 1
        rect = Rectangle(170, 25, self.cell_size, self.cell_size, self.current_color)
        rect.draw(self.info_panel)
        self.info_panel.fill_rect(rect, self.current_color)

    def get_color(self, p):
        x, y = p.conv()
        if y > 80:
            return self.current_color
        if self.margin <= x <= self.cell_size * 4 + self.margin * 4:
            col = int((x - self.margin / 2) // (self.margin + self.cell_size))
            row = int((y - self.margin / 2) // (self.margin + self.cell_size))
            ix = x - col * ( self.margin + self.cell_size) - self.margin / 2
            iy = y - row * ( self.margin + self.cell_size) - self.margin / 2
            if self.margin / 2 <= ix <= self.cell_size and self.margin / 2 <= iy <= self.cell_size:
                return self.colors[4 * row + col]
        return self.current_color




class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.active = False
        self.rect = Rectangle(x, y, self.width, self.height, color)

    def draw(self, surface):
        surface.fill_rect(self.rect, self.color)
        if self.active:
            x, y = self.x, self.y
            width, height = self.width - 1, self.height - 1
            draw_line_dda(surface, Point2D(x, y), Point2D(x + width, y), cn.GREEN, antialiasing=False)
            draw_line_dda(surface, Point2D(x, y + height), Point2D(x + width, y + height), cn.GREEN, antialiasing=False)
            draw_line_dda(surface, Point2D(x, y), Point2D(x, y + height), cn.GREEN, antialiasing=False)
            draw_line_dda(surface, Point2D(x + width, y), Point2D(x + width, y + height), cn.GREEN, antialiasing=False)

    def is_clicked(self, point):
        px, py = point.conv()
        return self.x <= px < self.x + self.width and self.y <= py < self.y + self.height




class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y




class Point2D(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y

    def conv(self):
        return self.x, self.y

    def move_by_vector(self, vector):
        return Point2D(self.x + vector.dx, self.y - vector.dy)




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
            draw_line_dda(surface, p1, p2, self.color, antialiasing=False)




class Parallelogram(Polygon2D):
    def __init__(self, p1, p2, p3, p4, color):
        points = [p1, p2, p3, p4]
        super().__init__(color, points)




class Rectangle(Parallelogram):
    def __init__(self, x, y, width, height, color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        p1 = Point2D(x, y)
        p2 = Point2D(x + width - 1, y)
        p3 = Point2D(x + width - 1, y + height - 1)
        p4 = Point2D(x, y + height - 1)
        super().__init__(p1, p2, p3, p4, color)




class Rhombus(Parallelogram):
    def __init__(self, center, width, height, color):
        cx, cy = center.conv()
        p1 = Point2D(cx, cy - height // 2)
        p2 = Point2D(cx + width // 2, cy)
        p3 = Point2D(cx, cy + height // 2)
        p4 = Point2D(cx - width // 2, cy)
        super().__init__(p1, p2, p3, p4, color)




class Circle(Shape):
    def __init__(self, center, radius, color):
        super().__init__(color)
        self.center = center
        self.radius = radius

    def draw(self, surface):
        cx, cy = self.center.conv()
        r = self.radius
        r2 = r * r
        for x in range(cx - r, cx + r + 1):
            for y in range(cy - r, cy + r + 1):
                dx = x - cx
                dy = y - cy
                if abs(dx*dx + dy*dy - r2) <= r:
                    surface.set_pixel(x, y, self.color)




class Square(Rhombus):
    def __init__(self, center, size,  color):
        super().__init__(center, size, size, color)




class Vector:
    pass



class Vector2D(Vector):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    @classmethod
    def from_angle(cls, len, digree):
        r = math.radians(digree)
        dx = len * math.cos(r)
        dy = len * math.sin(r)
        return cls(dx, dy)

    def __str__(self):
        return f"({self.dx}, {self.dy})"

    @property
    def length(self):
        return (self.dx ** 2 + self.dy ** 2) ** 0.5

    @property
    def angle(self):
        return math.degrees(math.atan2(self.dy, self.dx))

    def __add__(self, other):
        return Vector2D(self.dx + other.dx, self.dy + other.dy)

    def __sub__(self, other):
        return Vector2D(self.dx - other.dx, self.dy - other.dy)



