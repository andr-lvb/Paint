from Geometry import Point2D, Vector2D

import Constant as Cn
import math


class Turtle:
    def __init__(self, x, y, degree, draw=False):
        self.angle = math.radians(degree) # угол в радианах
        self.vector = Vector2D.from_angle(1, degree) # единичный вектор
        self.draw_flag = draw # рисовать ли след
        self.commands = [] # список команд (имя, значение)
        self.p = Point2D(x, y)  # текущее положение
        self.x = self.p.x
        self.y = self.p.y



    # Обновляет единичный вектор на основе текущего угла
    def _update_vector(self):
        self.vector = Vector2D(math.cos(self.angle), math.sin(self.angle))


    # Разбирает строку команд (по знаку "=")
    def parse(self, s):
        s = s.split()
        for a in s:
            a = a.split('=')
            self.commands.append((a[0], int(a[1])))


    # Перемещает черепаху вперёд на distance пикселей
    def forward(self, distance):
        v = self.vector * distance
        self.p = self.p.move_by_vector(v)


    # Перемещает черепаху назад на distance пикселей
    def backward(self, distance):
        v = self.vector * (-distance)
        self.p = self.p.move_by_vector(v)


    # Поворачивает черепаху влево на angle градусов
    def left(self, angle):
        radians = math.radians(angle)
        self.angle -= radians
        self._update_vector()


    # Поворачивает черепаху вправо на angle градусов
    def right(self, angle):
        radians = math.radians(angle)
        self.angle += radians
        self._update_vector()


    # Выполняет все команды без отрисовки
    def run(self):
        self.x = self.p.x
        self.y = self.p.y
        for cmd, val in self.commands:
            if cmd == 'forward':
                self.forward(val)
            elif cmd == 'backward':
                self.backward(val)
            elif cmd == 'left':
                self.left(val)
            elif cmd == 'right':
                self.right(val)


    # Отрисовывает начальную точку черным и конечную красным.
    def drawing(self, canvas):
        canvas.set_pixel(round(self.x), round(self.y), Cn.BLUE)
        canvas.set_pixel(round(self.p.x), round(self.p.y), Cn.RED)