import pygame as pg
import game as gm
import const as CN
from objects import Canvas
from draw import draw_line_dda
# инициализируем pygame
pg.init()

# создаем экран
screen = pg.display.set_mode((800, 880))
canvas = Canvas(screen, CN.WIDTH, CN.HEIGHT)
# название для игры
pg.display.set_caption('Paint')

# таймер для контроля фпс
clock = pg.time.Clock()

running = True

point = 0
list_point = []

while running:
    for event in pg.event.get():
        # событие - выход из игры
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.MOUSEBUTTONDOWN:
            p = canvas.get_coords()
            x, y = p.conv()
            if not point:
                if event.button == 1:
                    canvas.set_pixel(x, y, (255,0,0))
                elif event.button == 3:
                    canvas.set_pixel(x, y)
            else:
                list_point.append(p)
                point -= 1
                if point == 0:
                    draw_line_dda(canvas, list_point[0], list_point[1],(0,255,0))
                    list_point = []

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_r:
                point = 2














    canvas.draw()

    # обновление экрана (что бы отображалось нарисованное)
    pg.display.flip()

    # устанавливаем кол-во кадров не более 60
    clock.tick(60)
