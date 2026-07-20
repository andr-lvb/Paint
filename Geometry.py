from Draw import draw_line_dda
from collections import deque

import math


# точка с координатами x, y
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y





# Двумерная точка. Может возвращать кортеж, перемещаться по вектору
class Point2D(Point):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.x = x
        self.y = y


    # Возвращает координаты в виде кортежа (x, y)
    def conv(self):
        return self.x, self.y

    # Смещает точку на заданный вектор
    def move_by_vector(self, vector):
        return Point2D(self.x + vector.dx, self.y - vector.dy)


    def __str__(self):
        return f'({self.x}, {self.y})'





class Vector:
    pass


# Двумерный вектор с операциями и методами угла/длины
class Vector2D(Vector):
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy


    # Создаёт вектор по длине и углу в градусах (от оси X)
    @classmethod
    def from_angle(cls, length, degree):
        r = math.radians(degree)
        dx = length * math.cos(r)
        dy = length * math.sin(r)
        return cls(dx, dy)


    # Длина вектора
    @property
    def length(self):
        return (self.dx ** 2 + self.dy ** 2) ** 0.5


    # Угол вектора в градусах (от оси X)
    @property
    def angle(self):
        return math.degrees(math.atan2(self.dy, self.dx))


    def __add__(self, other):
        return Vector2D(self.dx + other.dx, self.dy + other.dy)


    def __sub__(self, other):
        return Vector2D(self.dx - other.dx, self.dy - other.dy)


    def __mul__(self, other):
        return Vector2D(self.dx * other, self.dy * other)


    def __str__(self):
        return f"({self.dx}, {self.dy})"




# Отрезок, заданный двумя точками и цветом
class Line:
    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.p2 = p2
        self.color = color


    def __str__(self):
        return f'({self.p1}, {self.p2}, {self.color})'




# Базовый класс для всех фигур
class Shape:
    def __init__(self, color):
        self.color = color


    def draw(self, surface):
        pass





# Фигура на плоскости, заданная набором точек
class Shape2D(Shape):
    def __init__(self, color, points):
        super().__init__(color)
        self.points = points





# Многоугольник, рисуется замкнутой ломаной
class Polygon2D(Shape2D):
    def __init__(self, color, points):
        super().__init__(color, points)


    def draw(self, surface):
        if len(self.points) < 2:
            return
        # Соединяем точки попарно с замыканием
        for i in range(len(self.points)):
            p1 = self.points[i]
            p2 = self.points[(i + 1) % len(self.points)]
            draw_line_dda(surface, p1, p2, self.color, antialiasing=False)


    # Заливка замкнутой области
    @classmethod
    def fill(cls, surface, p, color):
        old_color = surface.get_pixel(p.x, p.y)
        d = [(1,0), (0,1), (0,-1), (-1, 0)]
        q = deque([p])
        surface.set_pixel(q[0].x, q[0].y, color)

        while q:
            current = q.popleft()

            for dx,dy in d:
                x, y = current.x + dx, current.y + dy

                if old_color == surface.get_pixel(x, y):
                    surface.set_pixel(x, y, color)
                    q.append(Point2D(x, y))





# Параллелограмм, заданныйпо четырём точкам
class Parallelogram(Polygon2D):
    def __init__(self, p1, p2, p3, p4, color):
        points = [p1, p2, p3, p4]
        super().__init__(color, points)





# Прямоугольник, заданный левым верхним углом (x, y), шириной и высотой
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





# Ромб, заданный по центру, ширине и высоте
class Rhombus(Parallelogram):
    def __init__(self, center, width, height, color):
        cx, cy = center.conv()
        p1 = Point2D(cx, cy - height // 2)
        p2 = Point2D(cx + width // 2, cy)
        p3 = Point2D(cx, cy + height // 2)
        p4 = Point2D(cx - width // 2, cy)
        super().__init__(p1, p2, p3, p4, color)




# Окружность заданного радиуса
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
                # Если расстояние от центра примерно равно радиусу
                if abs(dx*dx + dy*dy - r2) <= r:
                    surface.set_pixel(x, y, self.color)




# Квадрат как частный случай ромба с равными сторонами
class Square(Rhombus):
    def __init__(self, center, size,  color):
        super().__init__(center, size, size, color)