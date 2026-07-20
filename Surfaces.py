from Geometry import Point2D

import Constant as Cn
import pygame as pg


# Базовая панель с пиксельной сеткой.  Хранит двумерный список цветов и отображается на Surface
class Panel:
    def __init__(self, screen, width, height, bg_color=Cn.WHITE):
        self.width = width # Ширина в пикселях (Info_Panel) или в клетках (Canvas)
        self.height = height # Высота аналогично
        self.screen = screen # Главный экран pygame
        self.bg_color = bg_color # Бекграунд цвет (по умолчанию белый)
        self.pixels = [[bg_color for _ in range(width)] for _ in range(height)] # Марица цветов (height, width)
        self.surface = pg.Surface((self.width, self.height)) # Поверхность для прямого рисования
        self.surface.fill(self.bg_color) # Заливаем поверхность для прямого рисования (фоновым цветом панели)


    def get_coords(self):
        pass


    # Получить цвет пикселя по координатам
    def get_pixel(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.pixels[y][x]
        return None


    # Установить цвет пикселя. Если цвет не задан, используется фоновый цвет панели
    def set_pixel(self, x, y, color=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            color1 = color if color is not None else self.bg_color
            self.pixels[y][x] = color1
            self.surface.set_at((x, y), color1)


    def draw(self):
        pass


    # Заливает прямоугольную область Rectangle указанным цветом.
    def fill_rect(self, rect, color):
        for r in range(rect.height):
            for c in range(rect.width):
                self.set_pixel(rect.x + c, rect.y + r, color)





# Холст для рисования, состоящий из клеток размером CELL_SIZE. Ширина и высота задаются в количестве клеток
class Canvas(Panel):
    def __init__(self, screen, width, height, bg_color=Cn.WHITE):
        super().__init__(screen, width, height, bg_color)
        self.surface = pg.Surface((self.width * Cn.CELL_SIZE, self.height * Cn.CELL_SIZE))  # Переопределяем surface
        self.surface.fill(self.bg_color)
        self.grid_surface = None


    # Возвращает координаты мыши в клетках холста. Учитывает смещение по вертикали (80 пикселей верхней панели)
    def get_coords(self):
        x, y = pg.mouse.get_pos()
        canvas_x = x // Cn.CELL_SIZE
        canvas_y = (y - 80) // Cn.CELL_SIZE
        return Point2D(canvas_x, canvas_y)


    # Рисует одну клетку (x,y) на холсте
    def set_pixel(self, x, y, color=None):
        if 0 <= x < self.width and 0 <= y < self.height:
            color1 = color if color is not None else self.bg_color
            # Рисуем прямоугольник на масштабированной поверхности
            rect = pg.Rect(x * Cn.CELL_SIZE, y * Cn.CELL_SIZE, Cn.CELL_SIZE, Cn.CELL_SIZE)
            # Обновляем матрицу цветов
            self.pixels[y][x] = color1
            self.surface.fill(color1, rect)


    # Отображает холст на главном экране со смещением 80 пикселей сверху
    def draw(self):
        self.screen.blit(self.surface, (0, 80))
        if Cn.CELL_SIZE >= 3:
            if self.grid_surface is None:
                self.grid_surface = self.draw_grid()
            self.screen.blit(self.grid_surface, (0, 80))


    # Создаёт и возвращает прозрачную поверхность с линиями сетки
    def draw_grid(self):
        width = self.width * Cn.CELL_SIZE
        height = self.height * Cn.CELL_SIZE
        grid = pg.Surface((width, height), pg.SRCALPHA)

        for x in range(0, width, Cn.CELL_SIZE):
            pg.draw.line(grid, Cn.COLOR_LINE, (x, 0), (x, height))

        for y in range(0, height, Cn.CELL_SIZE):
            pg.draw.line(grid, Cn.COLOR_LINE, (0, y), (width, y))
        return grid




# Верхняя информационная панель
class Info_Panel(Panel):
    def __init__(self, screen, width, height, bg_color=Cn.BLACK):
        super().__init__(screen, width, height, bg_color)


    # Отрисовка панели в левом верхнем углу
    def draw(self):
       self.screen.blit(self.surface, (0, 0))


    # Возвращает координаты мыши
    def get_coords(self):
        x, y = pg.mouse.get_pos()
        return Point2D(x, y)