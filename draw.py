import math




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
        if 0 <= int(x0) < surface.width and 0 <= int(y0) < surface.height:
            surface.set_pixel(int(x0), int(y0), color)
        return

    x_i = dx / steps
    y_i = dy / steps
    x, y = float(x0), float(y0)

    for _ in range(steps + 1):
        ix = int(round(x))
        iy = int(round(y))
        if not (0 <= ix < surface.width and 0 <= iy < surface.height):
            x += x_i
            y += y_i
            continue

        if antialiasing and thickness == 1:
            if abs(dx) > abs(dy):
                err = y - math.floor(y) - 0.5
                intensity = abs(err)
                surface.set_pixel(ix, iy, color)
                if err > 0:
                    ny = iy + 1
                else:
                    ny = iy - 1
                if 0 <= ny < surface.height:
                    blend_pixel(surface, ix, ny, color, intensity)
            else:
                err = x - math.floor(x) - 0.5
                intensity = abs(err)
                surface.set_pixel(ix, iy, color)
                if err > 0:
                    nx = ix + 1
                else:
                    nx = ix - 1
                if 0 <= nx < surface.width:
                    blend_pixel(surface, nx, iy, color, intensity)
        else:
            half = thickness // 2
            for dy_off in range(-half, half + 1):
                for dx_off in range(-half, half + 1):
                    px = ix + dx_off
                    py = iy + dy_off
                    if 0 <= px < surface.width and 0 <= py < surface.height:
                        surface.set_pixel(px, py, color)
        x += x_i
        y += y_i