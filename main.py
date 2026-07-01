import pygame as pg
import const as cn
from objects import Canvas, Palette, Info_Panel, Circle, Button
from draw import draw_line_dda

# инициализируем pygame
pg.init()

# создаем экран screen
screen = pg.display.set_mode((800, 880))

# создаем экран canvas
canvas = Canvas(screen, cn.WIDTH, cn.HEIGHT)

# создаем экран info panel
info_panel = Info_Panel(screen, 800, 80)

# создаем меню palette
palette = Palette(info_panel, cn.PALETTE_COLORS, 800, 80)

# создаем ластик
eraser_button = Button(240, 20, 40, 40, cn.GRAY)

# устанавливаем название для игры
pg.display.set_caption('Paint')

# таймер для контроля фпс
clock = pg.time.Clock()

running = True
point = 0
list_point = []
eraser_mode = False
eraser_radius = 20

def create_eraser_cursor(radius, cell_size):
    size = radius * 2 * cell_size
    surface = pg.Surface((size, size), pg.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    pg.draw.circle(surface, (255, 0, 0, 100), (size//2, size//2), radius*cell_size, 1)
    pg.draw.circle(surface, (255, 0, 0, 30), (size//2, size//2), radius*cell_size)
    return pg.cursors.Cursor((size//2, size//2), surface)

while running:
    for event in pg.event.get():
        # событие - выход из игры
        if event.type == pg.QUIT:
            running = False

        # p = canvas.get_coords()
        # x, y = p.conv()
        # draw_line_dda(canvas, Point2D(0,0), p, cn.RED)

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()

            if mouse_y < 80:
                p_info = info_panel.get_coords()
                palette.current_color = palette.get_color(p_info)

                if eraser_button.is_clicked(p_info):
                    eraser_mode = not eraser_mode
                    eraser_button.active = eraser_mode

                    if eraser_mode:
                        point = 0
                        list_point = []
                        pg.mouse.set_cursor(create_eraser_cursor(eraser_radius, cn.CELL_SIZE))

                    else:
                        pg.mouse.set_cursor(pg.cursors.arrow)

            else:
                if event.button == 1 and eraser_mode:
                    p = canvas.get_coords()
                    cx, cy = p.conv()
                    for dy in range(-eraser_radius, eraser_radius + 1):
                        for dx in range(-eraser_radius, eraser_radius + 1):
                            if dx * dx + dy * dy <= eraser_radius * eraser_radius:
                                canvas.set_pixel(cx + dx, cy + dy, canvas.bg_color)

                else:
                    p = canvas.get_coords()
                    x, y = p.conv()

                    if not point:
                        if event.button == 1:
                            canvas.set_pixel(x, y, cn.RED)

                        elif event.button == 2:
                            circle = Circle(p, 200, cn.RED)
                            circle.draw(canvas)

                        elif event.button == 3:
                            canvas.set_pixel(x, y)

                    else:
                        if event.button == 1:
                            list_point.append(p)
                            point -= 1
                            if point == 0:
                                draw_line_dda(canvas, list_point[0], list_point[1], cn.GREEN)
                                list_point = []

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        point = 2
                        list_point = []

        if event.type == pg.MOUSEMOTION and eraser_mode:
            if event.buttons[0] == 1:
                p = canvas.get_coords()
                cx, cy = p.conv()
                for dy in range(-eraser_radius, eraser_radius + 1):
                    for dx in range(-eraser_radius, eraser_radius + 1):
                        if dx * dx + dy * dy <= eraser_radius * eraser_radius:
                            canvas.set_pixel(cx + dx, cy + dy, canvas.bg_color)


    # отрисовываем все поверхности
    canvas.draw()
    info_panel.draw()
    palette.draw()

    eraser_button.draw(info_panel)

    # обновление экрана (что бы отображалось нарисованное)
    pg.display.flip()

    # устанавливаем кол-во кадров не более 60
    clock.tick(60)
