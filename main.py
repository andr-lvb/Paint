import pygame as pg
import const as cn
from objects import Canvas, Palette, Info_Panel, Circle, Button, Vector2D, Point2D, Line, Turtle, Polygon2D
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

# создаем конпку ластика
eraser_button = Button(240, 10, 60, 60, cn.GRAY)

# создаем конпку для измнения линии
edit_button = Button(350, 10, 60, 60, cn.BLUE)

# устанавливаем название для игры
pg.display.set_caption('Paint')

# таймер для контроля фпс
clock = pg.time.Clock()

running = True
edit_mode = False
eraser_mode = False
dragging_end = False
anchor_point = None
previous_drag_point = None
fill = False


selected_end = 0
point = 0
selected_line_index = -1
eraser_radius = 2
count = 0

list_point = []
lines = []

turtle1 = Turtle(50,20,0)
# s = 'forward=10\nbackward=4\nleft=60\nright=30'
file = open('turtl')
s = ''.join(file.readlines())
turtle1.parse(s)



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

        if event.type == pg.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pg.mouse.get_pos()

            if mouse_y < 80:
                p_info = info_panel.get_coords()
                palette.current_color = palette.get_color(p_info)

                if eraser_button.is_clicked(p_info):
                    eraser_mode = not eraser_mode
                    eraser_button.active = eraser_mode
                    edit_button.active = False
                    edit_mode = False

                    if eraser_mode:
                        pg.mouse.set_cursor(create_eraser_cursor(eraser_radius, cn.CELL_SIZE))

                    else:
                        pg.mouse.set_cursor(pg.cursors.arrow)

                if edit_button.is_clicked(p_info):
                    edit_mode = not edit_mode
                    edit_button.active = edit_mode

                    if edit_mode:
                        eraser_mode = False
                        eraser_button.active = False
                        point = 0
                        list_point = []
                        pg.mouse.set_cursor(pg.cursors.arrow)

                    else:
                        pg.mouse.set_cursor(pg.cursors.arrow)
                        selected_line_index = -1

            else:

                if event.button == 1 and eraser_mode:
                    p = canvas.get_coords()
                    cx, cy = p.conv()

                    for dy in range(-eraser_radius, eraser_radius + 1):
                        for dx in range(-eraser_radius, eraser_radius + 1):

                            if dx * dx + dy * dy <= eraser_radius * eraser_radius:
                                canvas.set_pixel(cx + dx, cy + dy, canvas.bg_color)


                elif edit_mode and event.button == 1:
                    p = canvas.get_coords()
                    cx, cy = p.conv()
                    minimum_distance = 2.5
                    found = None

                    for i, line in enumerate(lines):
                        for end_index, pt in enumerate([line.p1, line.p2]):
                            distance = max(abs(p.x - pt.x), abs(p.y - pt.y))

                            if distance < minimum_distance:
                                minimum_distance = distance
                                found = (i, end_index)

                            if found is not None:
                                selected_line_index, selected_end = found
                                line = lines[selected_line_index]
                                anchor_point = line.p2 if selected_end == 0 else line.p1
                                previous_drag_point = line.p1 if selected_end == 0 else line.p2
                                dragging_end = True


                elif not edit_mode and not eraser_mode:
                    p = canvas.get_coords()
                    x, y = p.conv()

                    if not point:

                        if event.button == 1:
                            if fill:
                                p = canvas.get_coords()
                                Polygon2D.fill(canvas, p, palette.current_color)
                                fill = False
                            canvas.set_pixel(x, y, palette.current_color)

                        elif event.button == 2:
                            circle = Circle(p, 20, palette.current_color)
                            circle.draw(canvas)

                        elif event.button == 3:
                            canvas.set_pixel(x, y)

                    else:
                        if event.button == 1:
                            list_point.append(p)
                            point -= 1
                            if point == 0:
                                draw_line_dda(canvas, list_point[0], list_point[1], palette.current_color, antialiasing=False)
                                lines.append(Line(list_point[0], list_point[1], palette.current_color))
                                list_point = []


        elif event.type == pg.MOUSEMOTION and eraser_mode:
            if event.buttons[0] == 1:
                p = canvas.get_coords()
                cx, cy = p.conv()
                for dy in range(-eraser_radius, eraser_radius + 1):
                    for dx in range(-eraser_radius, eraser_radius + 1):
                        if dx * dx + dy * dy <= eraser_radius * eraser_radius:
                            canvas.set_pixel(cx + dx, cy + dy, canvas.bg_color)


        elif event.type == pg.MOUSEMOTION and edit_mode and dragging_end and event.buttons[0] == 1:
            current_point = canvas.get_coords()
            draw_line_dda(canvas, anchor_point, previous_drag_point, canvas.bg_color, antialiasing=False)
            draw_line_dda(canvas, anchor_point, current_point, lines[selected_line_index].color, antialiasing=False)
            previous_drag_point = current_point


        elif event.type == pg.MOUSEBUTTONUP:
            if event.button == 1 and dragging_end:
                line = lines[selected_line_index]
                if selected_end == 0:
                    line.p1 = previous_drag_point

                else:
                    line.p2 = previous_drag_point
                    dragging_end = False
                    selected_line_index = -1
                    anchor_point = None
                    previous_drag_point = None


        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r and not edit_mode and not eraser_mode:
                point = 2
                list_point = []

            if event.key == pg.K_t and not edit_mode and not eraser_mode:
                p1 = Point2D(4, 5)
                v = Vector2D.from_angle(10, -45)
                p2 = p1.move_by_vector(v)
                draw_line_dda(canvas, p1, p2, palette.current_color)

            if event.key == pg.K_y:
                if count == 0:
                    turtle1.Draw(canvas)
                    turtle1.run()
                    count += 1
                if count == 1:
                    turtle1.Draw(canvas)
                    count = 0

            if event.key == pg.K_f:
                fill = True







        # отрисовываем все поверхности и кнопки
    canvas.draw()
    info_panel.draw()
    palette.draw()
    edit_button.draw(info_panel)
    eraser_button.draw(info_panel)

    if edit_mode and dragging_end and selected_line_index != -1:
        sx = previous_drag_point.x * cn.CELL_SIZE + cn.CELL_SIZE // 2
        sy = previous_drag_point.y * cn.CELL_SIZE + 80 + cn.CELL_SIZE // 2
        pg.draw.circle(screen, (255, 0, 0), (sx, sy), 6, 2)

    # обновление экрана (что бы отображалось нарисованное)
    pg.display.flip()

    # устанавливаем кол-во кадров не более 60
    clock.tick(60)
