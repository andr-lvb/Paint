from Geometry import Rectangle, Point2D
from Draw import draw_line_dda

import Constant as Cn


# Прямоугольная кнопка c рамкой при активации.
class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.active = False # активно ли состояние (переключено)
        self.rect = Rectangle(x, y, self.width, self.height, color)

    # Отрисовывает кнопку на заданной поверхности (Panel)
    def draw(self, surface):
        surface.fill_rect(self.rect, self.color)
        # Если кнопка активна, рисуем зелёную рамку
        if self.active:
            x, y = self.x, self.y
            width, height = self.width - 1, self.height - 1
            # Верхняя граница
            draw_line_dda(surface, Point2D(x, y), Point2D(x + width, y), Cn.GREEN, antialiasing=False)
            # Нижняя граница
            draw_line_dda(surface, Point2D(x, y + height), Point2D(x + width, y + height), Cn.GREEN, antialiasing=False)
            # Левая граница
            draw_line_dda(surface, Point2D(x, y), Point2D(x, y + height), Cn.GREEN, antialiasing=False)
            # Правая граница
            draw_line_dda(surface, Point2D(x + width, y), Point2D(x + width, y + height), Cn.GREEN, antialiasing=False)

    # Проверяет, находится ли точка point внутри кнопки
    def is_clicked(self, point):
        px, py = point.conv()
        return self.x <= px < self.x + self.width and self.y <= py < self.y + self.height





# Палитра цветов, отображаемая на верхней панели.
# Содержит ячейки с цветами и кнопку с текущим выбранным цветом
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


# Отрисовывает палитру на Info_Panel.
    def draw(self):
        cols = 4
        rows = 2
        start_x = self.margin
        start_y = self.margin
        i = 0
        # Рисуем 8 ячеек с цветами
        for r in range(rows):
            for c in range(cols):
                x = start_x + c * (self.cell_size + self.margin)
                y = start_y + r * (self.cell_size + self.margin)
                rect = Rectangle(x, y, self.cell_size, self.cell_size, self.colors[i])
                rect.draw(self.info_panel)
                # Заполняем прямоугольник цветом на панели
                self.info_panel.fill_rect(rect, self.colors[i])
                i += 1

        # Отдельный прямоугольник с текущим цветом (справа)
        current_rect = Rectangle(170, 25, self.cell_size, self.cell_size, self.current_color)
        current_rect.draw(self.info_panel)
        self.info_panel.fill_rect(current_rect, self.current_color)

    # Определяет, по какой ячейке палитры кликнули, и возвращает выбранный цвет.
    # Если клик вне палитры, возвращает текущий цвет
    def get_color(self, p):
        x, y = p.conv()

        if y > 80:
            return self.current_color
        # Проверяем, попадает ли клик в область палитры
        if self.margin <= x <= self.cell_size * 4 + self.margin * 4:
            col = int((x - self.margin / 2) // (self.margin + self.cell_size))
            row = int((y - self.margin / 2) // (self.margin + self.cell_size))
            ix = x - col * (self.margin + self.cell_size) - self.margin / 2
            iy = y - row * (self.margin + self.cell_size) - self.margin / 2
            if self.margin / 2 <= ix <= self.cell_size and self.margin / 2 <= iy <= self.cell_size:
                return self.colors[4 * row + col]
        return self.current_color
