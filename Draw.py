import math

# Смешивает цвет пикселя с заданным цветом с учётом интенсивности (0.1)
def blend_pixel(surface, x, y, color, intensity):
    if 0 <= x < surface.width and 0 <= y < surface.height:
        existing = surface.get_pixel(x, y)
        r = int(existing[0] * (1 - intensity) + color[0] * intensity)
        g = int(existing[1] * (1 - intensity) + color[1] * intensity)
        b = int(existing[2] * (1 - intensity) + color[2] * intensity)
        surface.set_pixel(x, y, (r, g, b))





def draw_line_dda(surface, p1, p2, color, thickness=1, antialiasing=True):
    x0, y0 = p1.conv()
    x1, y1 = p2.conv()
    dx = x1 - x0
    dy = y1 - y0
    steps = int(max(abs(dx), abs(dy)))

    if steps == 0:
        # Отрезок нулевой длины – одна точка
        if 0 <= x0 < surface.width and 0 <= y0 < surface.height:
            surface.set_pixel(int(x0), int(y0), color)
        return


    line_pixels = set()
    line_pixels_list = []

    x_inc = dx / steps
    y_inc = dy / steps
    x, y = float(x0), float(y0)

    for _ in range(steps + 1):
        ix = int(round(x))
        iy = int(round(y))
        if 0 <= ix < surface.width and 0 <= iy < surface.height:
            if (ix, iy) not in line_pixels:
                line_pixels.add((ix, iy))
                line_pixels_list.append((ix, iy))
        x += x_inc
        y += y_inc


    if thickness > 1:
        half = thickness // 2
        # создаём множество для толстой линии
        thick_pixels = set(line_pixels)
        for (ix, iy) in line_pixels_list:
            for dx_off in range(-half, half + 1):
                for dy_off in range(-half, half + 1):
                    nx, ny = ix + dx_off, iy + dy_off
                    if 0 <= nx < surface.width and 0 <= ny < surface.height:
                        thick_pixels.add((nx, ny))

        drawing_pixels = thick_pixels
    else:
        drawing_pixels = line_pixels

    for (ix, iy) in drawing_pixels:
        surface.set_pixel(ix, iy, color)

    if antialiasing:

        directions = [
            (1, 0, 0.3), (-1, 0, 0.3), (0, 1, 0.3), (0, -1, 0.3),  # ортогональные
            # (1, 1, 0.15), (-1, 1, 0.15), (1, -1, 0.15), (-1, -1, 0.15)  # диагонали
        ]

        for (ix, iy) in drawing_pixels:
            for dx_dir, dy_dir, intensity in directions:
                nx, ny = ix + dx_dir, iy + dy_dir
                if 0 <= nx < surface.width and 0 <= ny < surface.height:
                    if (nx, ny) not in drawing_pixels:
                        blend_pixel(surface, nx, ny, color, intensity)